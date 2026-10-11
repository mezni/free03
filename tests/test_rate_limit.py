import pytest

from ticket_triage.rate_limit import (
    ConcurrencyLimitExceededError,
    ConcurrencyLimiter,
    LocalRateLimitExceededError,
    TokenBucket,
)


def test_token_bucket_allows_initial_burst():
    bucket = TokenBucket(
        capacity=2,
        refill_rate_per_second=1,
        clock=lambda: 100.0,
    )

    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert not bucket.try_acquire()


def test_token_bucket_refills_over_time():
    now = [100.0]
    bucket = TokenBucket(
        capacity=2,
        refill_rate_per_second=1,
        clock=lambda: now[0],
    )

    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert not bucket.try_acquire()

    now[0] += 1.0

    assert bucket.try_acquire()
    assert not bucket.try_acquire()


def test_token_bucket_caps_refill_at_capacity():
    now = [100.0]
    bucket = TokenBucket(
        capacity=2,
        refill_rate_per_second=1,
        clock=lambda: now[0],
    )

    now[0] += 100
    assert bucket.try_acquire()
    assert bucket.try_acquire()
    assert not bucket.try_acquire()


def test_concurrency_limiter_runs_operation():
    limiter = ConcurrencyLimiter(max_concurrent=1)

    assert limiter.run(lambda: "done") == "done"


def test_concurrency_limiter_rejects_when_permit_unavailable():
    limiter = ConcurrencyLimiter(max_concurrent=1)
    assert limiter.semaphore.acquire(blocking=False)

    try:
        with pytest.raises(ConcurrencyLimitExceededError):
            limiter.run(
                lambda: "should not run",
                acquire_timeout_seconds=0,
            )
    finally:
        limiter.semaphore.release()


def test_concurrency_permit_is_released_after_error():
    limiter = ConcurrencyLimiter(max_concurrent=1)

    def failing_operation():
        raise ValueError("expected failure")

    with pytest.raises(ValueError):
        limiter.run(failing_operation)

    assert limiter.run(lambda: "recovered") == "recovered"


def test_local_rate_limit_exceeded_is_runtime_error():
    exc = LocalRateLimitExceededError("rate limited")
    assert str(exc) == "rate limited"
    assert isinstance(exc, RuntimeError)