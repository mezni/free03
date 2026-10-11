import pytest

from ticket_triage.deadlines import (
    DeadlineExceededError,
    call_with_deadline,
)


def test_operation_timeout_is_bounded_by_remaining_budget():
    received_timeouts = []

    result = call_with_deadline(
        lambda timeout: received_timeouts.append(timeout) or "ok",
        deadline=105.0,
        clock=lambda: 100.0,
        max_attempt_timeout_seconds=10.0,
    )

    assert result == "ok"
    assert received_timeouts == [5.0]


def test_operation_timeout_uses_per_attempt_limit():
    received_timeouts = []

    call_with_deadline(
        lambda timeout: received_timeouts.append(timeout),
        deadline=120.0,
        clock=lambda: 100.0,
        max_attempt_timeout_seconds=8.0,
    )

    assert received_timeouts == [8.0]


def test_expired_deadline_does_not_start_operation():
    calls = []

    with pytest.raises(DeadlineExceededError):
        call_with_deadline(
            lambda timeout: calls.append(timeout),
            deadline=100.0,
            clock=lambda: 100.0,
        )

    assert calls == []


def test_remaining_budget_is_used_when_smaller_than_per_attempt_limit():
    received_timeouts = []

    result = call_with_deadline(
        lambda timeout: received_timeouts.append(timeout) or "ok",
        deadline=105.0,
        clock=lambda: 100.0,
        max_attempt_timeout_seconds=20.0,
    )

    assert result == "ok"
    assert received_timeouts == [5.0]


def test_negative_remaining_deadline_raises():
    with pytest.raises(DeadlineExceededError):
        call_with_deadline(
            lambda timeout: timeout,
            deadline=50.0,
            clock=lambda: 60.0,
        )


def test_zero_remaining_deadline_raises():
    with pytest.raises(DeadlineExceededError):
        call_with_deadline(
            lambda timeout: timeout,
            deadline=100.0,
            clock=lambda: 100.0,
        )