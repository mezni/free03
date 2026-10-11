# Day 11 — Resilience and Error Handling

## Objective

Make classification and routing failures explicit, bounded, and safe.

## Implemented

- Introduced typed provider errors (`errors.py`).
- Preserved transient and permanent failure distinctions.
- Added a bounded retry wrapper for transient classification failures.
- Mapped selected OpenAI connection, timeout, and rate-limit exceptions.
- Defined safe handling for unknown routing outcomes.
- Added retry behavior tests.

## Architecture concepts

### Fault isolation

Provider failures should not corrupt the domain model or silently bypass policy. Provider errors inherit from `ClassificationError`, so the existing application code that catches `ClassificationError` still sends known classification failures to manual review.

### Bounded retries

`RetryingClassifier` needs an attempt limit and an explicit definition of which errors are retryable. Only `TransientProviderError` is retried; malformed JSON, policy violations, and arbitrary exceptions are not. `max_attempts=2` means one initial attempt plus at most one retry.

### Idempotency and reconciliation

A timeout does not prove that a remote operation failed. Decision rule for routing:

- Confirmed failure before acceptance: retry only if known safe and still authorized.
- Confirmed success: mark routing successful and complete the case.
- Timeout or connection loss after submission: record `OUTCOME_UNKNOWN`; do not blindly resubmit.
- Reconciliation confirms the action did not happen: controlled retry may be possible.
- Reconciliation confirms success: record success without resubmitting.

The `OUTCOME_UNKNOWN` and `RECONCILIATION_REQUIRED` states from the Day 4 routing model exist for this reason. Durable idempotency keys and external operation identifiers are not yet implemented; an in-memory key alone does not prevent duplicates.

### Fail-safe behavior

If classification cannot produce a validated recommendation, the case should go to manual review rather than proceed automatically.

## Implementation details

- `LLMClassifier.classify()` now re-raises `TransientProviderError` and `PermanentProviderError` unchanged, and still wraps any other client exception in `ClassificationError`.
- `OpenAILLMClient.generate()` maps `APITimeoutError`, `APIConnectionError`, and `RateLimitError` to `TransientProviderError`, and rejects an empty `output_text` with `InvalidModelOutputError`. The exception names were confirmed against the installed SDK (openai 3.28.0).
- Retry wrapper composition: instrumentation inside the retry wrapper counts every provider attempt; instrumentation outside measures the user-visible duration.

## Testing

New and existing individual suites pass:

```text
$ python -m pytest tests/test_resilience.py tests/test_openai_client.py \
    tests/test_llm_classifier.py tests/test_observability.py tests/test_evaluation.py -q
....................                                                    [100%]
20 passed in 3.56s
```

The four new retry tests cover: retry-then-succeed on a transient failure, giving up after `max_attempts`, not retrying non-transient errors, and rejecting invalid configuration. The adapter now also has tests for transient-error mapping and empty-output rejection.

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR collecting tests/test_domain.py
ImportError: cannot import name 'validate_ticket' from 'ticket_triage.domain'
ERROR collecting tests/test_workflow.py
ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow'
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The full suite remains interrupted by the same pre-existing collection errors from Days 6-7. The expected cumulative count of 59 assumes an intact repository; the counts here reflect the partially built codebase.

## Limitations

- The retry wrapper uses a simple fixed delay.
- Provider exception mapping must be verified against the installed SDK (this is illustrative for openai 3.28.0).
- The SDK's own retry budget (configured in Day 9) and the application retry budget must be coordinated so they are not effectively multiplied.
- Routing reconciliation is not yet connected to a real ticketing provider.
- Durable idempotency and concurrent request protection are not yet implemented.
- The retry wrapper was composed in the documented snippet but not exercised through the application flow, which remains blocked by the Days 6-7 gaps.

## What I learned

Resilience is not simply retrying every failure. It is choosing the correct recovery behavior based on what is known about the operation's outcome.

## Next steps

- Add API-level integration tests.
- Persist routing operations and idempotency keys.
- Implement external-state reconciliation.
- Add exponential backoff, deadlines, and operational alerts.
- Resolve the Days 6-7 gaps (`validate_ticket`, `transition_case`, repository implementation, incomplete application service) so the full suite can run.

## Day 11 completion checklist

### Progress

6 of 7

- [x] Define typed errors
- [x] Update LLMClassifier to preserve provider error types
- [x] Implement RetryingClassifier
- [x] Map selected OpenAI transient errors
- [x] Add four retry tests
- [x] Run the full test suite (recorded; still blocked by pre-existing collection errors)
- [x] Write docs/progress/day-11.md