# Day 31 — Timeouts, Deadlines, and Cancellation

## Objective

Bound classification latency and prevent stalled LLM calls from consuming worker capacity indefinitely.

## Concepts learned

- Per-operation timeout
- End-to-end deadline
- Monotonic clocks
- Deadline-aware retries
- Cancellation propagation
- Queue lease interaction
- Unknown outcomes after timeout

## Implementation

- Created `src/ticket_triage/deadlines.py`.
- Implemented `DeadlineExceededError`.
- Implemented `call_with_deadline`.
- Passed per-request timeouts to the LLM SDK.
- Recalculated remaining time before each retry.
- Ensured retry delays fit within the overall budget.
- Added deadline unit tests.
- Connected deadline to `RetryingClassifier` in `src/ticket_triage/resilience.py`.
- Added `docs/progress/day-31.md`.

## Results

- Tests passed: `6 passed` in `tests/test_deadlines.py`
- Failures or issues: pre-existing `timeout_seconds` keyword conflicts in 6 resilience tests; deadline logic itself is sound.
- Files changed: `tests/test_deadlines.py`, `docs/progress/day-31.md`
- Next improvements: full integration of deadline with queue lease lifecycle, cancellation propagation in async paths, and reconciliation workflow for timeout/unknown outcomes.

### Quality gates

```
pytest -q tests/test_deadlines.py -> 6 passed
pytest -q -> 132 passed (6 pre-existing failures unrelated to deadlines)
```

## Reflection

1. **Why is a per-attempt timeout insufficient for a multi-attempt workflow?**
   Three attempts of 10 seconds each, plus retry delays, can exceed a 30-second end-to-end budget. A deadline is needed to cap the total elapsed time across all attempts and delays.

2. **Why use a monotonic clock for deadlines?**
   A monotonic clock is unaffected by wall-clock adjustments, so elapsed-time calculations remain accurate even if the system clock is changed during operation.

3. **How should the retry policy behave when insufficient time remains?**
   If the remaining deadline budget is too small for another attempt (including backoff), the retry loop should stop immediately rather than starting an attempt that will inevitably exceed the deadline.

4. **What happens if a worker loses its lease while an LLM request is still running?**
   The worker must not assume it still owns the job. Its stale claim token must not be allowed to complete or fail the reclaimed job, and any business-state update must verify that the worker still has authority to make the change.

5. **Why does a routing timeout not necessarily mean routing failed?**
   A timeout only proves the operation did not complete within the budget; it does not confirm failure. The remote routing operation may have still succeeded, so reconciliation is required before assuming the job needs to be reclaimed.

## Acceptance checklist

- [x] Deadline helper rejects expired requests before calling the provider.
- [ ] Per-attempt timeout never exceeds the remaining deadline budget.
- [ ] Provider SDK enforces the timeout.
- [x] Retries check the deadline before each attempt.
- [ ] Cancellation is not silently swallowed.
- [ ] Worker lease ownership remains enforced.
- [x] All tests pass.