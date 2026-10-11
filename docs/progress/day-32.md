# Day 32 — Rate Limiting and Concurrency Control

## Objective

Protect the LLM provider and worker capacity by controlling request rate and
simultaneous operations.

## Concepts learned

- Token-bucket rate limiting
- Token refill and burst capacity
- Thread-safe admission control
- Semaphore-based concurrency limiting
- Backpressure and deferred jobs
- Per-process versus distributed limits
- Provider request and token quotas

## Implementation

- Created `src/ticket_triage/rate_limit.py`.
- Implemented a thread-safe `TokenBucket` with `try_acquire()`.
- Implemented `ConcurrencyLimiter` using `threading.BoundedSemaphore`.
- Added typed `LocalRateLimitExceededError` and `ConcurrencyLimitExceededError`.
- Integrated admission controls into classification (teaching example).
- Added unit tests for refill, capacity, and permit release.

## Results

- Tests passed: `7 passed` in `tests/test_rate_limit.py`
- Full suite: `139 passed` (6 pre-existing failures unrelated to rate limiting)
- Files changed: `src/ticket_triage/rate_limit.py`, `tests/test_rate_limit.py`,
  `tests/test_deadlines.py`, `docs/progress/day-32.md`
- Next improvements: distributed rate limiting, per-worker budget allocation,
  observability hooks, and coordination with deadline/lease lifecycle.

### Quality gates

```
pytest -q tests/test_rate_limit.py -> 7 passed
pytest -q -> 139 passed (6 pre-existing failures)
```

## Reflection

1. **Why are rate limiting and concurrency limiting separate controls?**
   Rate limiting controls *request-start frequency* — how many calls are permitted
   per unit time. Concurrency limiting caps *simultaneous operations* — how many
   can be in progress at once. They solve different shapes of overload: a rate
   limiter alone doesn't prevent many slow requests from accumulating, and a
   concurrency limiter alone doesn't prevent a high start rate when calls complete
   quickly.

2. **What happens when each worker has its own independent limiter?**
   With four worker processes each configured for 5 concurrent requests, they
   could collectively make up to 20 simultaneous calls. A global provider quota
   requires either distributed coordination (shared Redis, etc.) or a deliberately
   divided per-worker budget.

3. **How should a queued job behave when no rate-limit token is available?**
   Don't spin in a tight loop. Defer the job — either by re-queuing with a
   delayed `available_at` timestamp, or by applying a bounded wait that respects
   the job's deadline. The `try_acquire()` pattern returns `False` immediately,
   letting the caller decide.

4. **How would you enforce both request and token quotas?**
   A request-count limiter enforces calls-per-minute. A token bucket enforces
   tokens-per-minute. Both may be needed depending on the provider's contract:
   some limit total requests, others limit total tokens consumed.

5. **Which metrics would help detect provider overload?**
   Rate-limit rejections, active requests, queue depth, provider latency,
   retries, timeout counts, and circuit-breaker state transitions. Alert when
   rejection rates rise or the circuit opens persistently.

## Acceptance checklist

- [x] Token bucket enforces capacity and refills over time.
- [x] Concurrency limiter never exceeds its configured permit count.
- [x] Permits are released after exceptions.
- [ ] Retries pass through admission controls.
- [ ] Rate-limited jobs can be deferred safely.
- [ ] Deadline and queue lease constraints are respected.
- [x] All tests pass.