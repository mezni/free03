# Day 30 — Retry Policies, Exponential Backoff, and Circuit Breakers

## Objective

Make the AI ticket-classification service resilient to temporary LLM provider
failures without creating retry storms or repeating unsafe operations.

## Concepts learned

- Transient versus permanent failures.
- Bounded retries with exponential backoff and full jitter.
- Circuit breaker states: `CLOSED`, `OPEN`, `HALF_OPEN`.
- Dependency failure isolation and failing fast.
- Retry budgets and coordinating SDK retries with application retries.

## Failure taxonomy

| Failure | Example | Correct response |
| --- | --- | --- |
| Transient | Rate limit, temporary connection error | Retry within a bounded limit |
| Permanent | Invalid credentials, unsupported request | Fail without retrying |
| Invalid model output | Malformed recommendation JSON | Treat as a classification failure; do not blindly retry |
| Unknown routing outcome | Routing provider timed out after receiving a request | Reconcile before retrying |

LLM classification retries and external routing retries are different problems.
Classification only produces a recommendation, so retrying is safe. Routing must
never be retried blindly when the first attempt may already have succeeded.

## Implementation

Replaced the fixed-delay `RetryingClassifier` in `src/ticket_triage/resilience.py`
with a bounded, backoff-based implementation, and added a circuit breaker:

- `RetryingClassifier`: exponential ceiling `min(max_delay, base * 2**(n-1))`
  with full jitter `random() * ceiling`. Only `TransientProviderError` is
  retried; the original exception propagates once the budget is exhausted.
  `sleep` and `random_fn` are injectable for deterministic tests.
- `CircuitBreakerClassifier`: `CLOSED` counts consecutive transient failures;
  at the threshold it moves to `OPEN` and fails fast with `CircuitOpenError`
  until the cooldown elapses; it then moves to `HALF_OPEN` and permits exactly
  one recovery probe. A successful probe closes the circuit; a failed probe
  reopens it. Non-transient errors do not count toward the threshold. State
  transitions are guarded by a lock that is never held during the provider call.
- Composition in `main.py`: `CircuitBreakerClassifier(RetryingClassifier(fake))`,
  so the breaker counts one *logical* request rather than each retry.

### Retry math

With a one-second base and eight-second cap, the pre-jitter ceilings are
`0–1s`, `0–2s`, `0–4s`, `0–8s` for retries 1–4. Jitter randomizes the actual
delay within each ceiling. Retries stay bounded by `max_attempts` and
`max_delay_seconds`.

## Design decisions

- The retry wrapper handles individual provider attempts; the circuit breaker
  counts the final result of one logical classification request. Composing the
  breaker outside prevents a single flaky logical request from tripping it.
- Permanent failures are not retried and do not open the circuit.
- Unknown routing outcomes require reconciliation, not blind retries.
- `CircuitState` is a `StrEnum` for consistency with the rest of the codebase.
- Because the OpenAI SDK may retry internally, application retries must be tuned
  so the two layers do not multiply provider calls.

## Tests

`tests/test_resilience.py` (13 tests) uses fake classifiers and an injected
clock, so no real API or waiting is involved:

- Transient failures retry and then succeed.
- Retries stop at `max_attempts`.
- Permanent and unexpected errors are not retried (no sleep occurs).
- Full-jitter backoff delays are deterministic (`[0.1, 0.2]`).
- Invalid retry configuration is rejected.
- The circuit opens at the threshold and rejects calls before the cooldown.
- A successful `HALF_OPEN` probe closes the circuit.
- A failed transient probe, and a failed permanent probe, reopen the circuit.
- Non-transient errors do not count toward the threshold.
- Only one half-open probe runs at a time.
- The breaker counts one failed logical request, not each retry (2 logical
  requests → 6 provider calls, then `OPEN`).
- Invalid breaker configuration (`failure_threshold=0`, `reset_timeout<=0`) is
  rejected.

## Results

- Tests passed: `132 passed` (123 pre-existing + 9 net new; 13 resilience tests).
- Failures or issues: none.
- Files changed: `src/ticket_triage/resilience.py`,
  `src/ticket_triage/main.py`, `tests/test_resilience.py`, this note.
- Next improvements: a sliding failure-counting window, retry/circuit metrics,
  cancellation behavior, and explicit coordination with SDK-level retries.

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 109 files already formatted
pytest                               -> 132 passed
```

## Reflection

1. **Why is jitter useful when many workers retry simultaneously?** Without
   jitter, workers that fail together retry together, producing synchronized
   bursts (a thundering herd) that keep an overloaded provider down. Randomizing
   the delay within the exponential ceiling spreads retries out and lets the
   provider recover.
2. **Why should a circuit breaker wrap the retry wrapper?** So the breaker counts
   one *logical* request's final outcome. If it wrapped the other way, every
   individual retry would count, tripping the breaker prematurely. Wrapping
   outside also lets the breaker fail fast before any retry budget is spent once
   the provider is known to be unhealthy.
3. **Difference between a transient provider error and an unknown routing
   outcome?** A transient provider error is a temporary failure with no side
   effect, so retrying is safe. An unknown routing outcome means the external
   system may already have performed the action; it must be reconciled with the
   provider before any retry, or a duplicate side effect could occur.
4. **How to measure retry count, circuit state, and provider failure rate?** Emit
   a counter for retry attempts labeled by outcome, expose circuit state as a
   gauge (`0` closed, `1` half-open, `2` open), and compute provider failure rate
   as failures divided by attempts over a rolling window; alert when the circuit
   is open and on sustained failure-rate increases.

## Acceptance checklist

- [x] Retry transient provider failures only.
- [x] Verify retries stop at `max_attempts`.
- [x] Verify permanent errors are not retried.
- [x] Verify backoff delays and jitter deterministically.
- [x] Verify the circuit opens after the configured failure threshold.
- [x] Verify `OPEN` rejects calls before cooldown expires.
- [x] Verify a successful `HALF_OPEN` probe closes the circuit.
- [x] Verify a failed probe reopens the circuit.
- [x] Run the full test suite and record the result (`132 passed`).

## Safety invariant

Resilience controls never bypass the human-approval requirement: classification
only produces a recommendation, and routing still requires a valid approval for
the current recommendation version.
