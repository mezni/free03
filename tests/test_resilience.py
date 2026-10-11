import pytest

from ticket_triage.domain import Priority, Recommendation, Ticket
from ticket_triage.errors import (
    PermanentProviderError,
    TransientProviderError,
)
from ticket_triage.resilience import (
    CircuitBreakerClassifier,
    CircuitOpenError,
    CircuitState,
    RetryingClassifier,
)


class SequenceClassifier:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def classify(self, ticket):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FlakyClassifier:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, ticket):
        self.calls += 1
        if self.calls == 1:
            raise TransientProviderError("Temporary failure")
        return Recommendation(
            category="billing",
            priority=Priority.HIGH,
            destination="billing-team",
            rationale="Synthetic test recommendation.",
        )


class AlwaysFailingClassifier:
    def __init__(self) -> None:
        self.calls = 0

    def classify(self, ticket):
        self.calls += 1
        raise TransientProviderError("Still unavailable")


def make_ticket():
    return Ticket(
        ticket_id="T-501",
        subject="Charged twice",
        description="I was charged twice for one order.",
    )


def test_retry_uses_exponential_backoff_with_full_jitter():
    classifier = SequenceClassifier(
        [
            TransientProviderError("temporary"),
            TransientProviderError("temporary"),
            "recommendation",
        ]
    )
    delays = []

    retrying = RetryingClassifier(
        classifier,
        max_attempts=3,
        base_delay_seconds=0.2,
        max_delay_seconds=1.0,
        sleep=delays.append,
        random_fn=lambda: 0.5,
    )

    assert retrying.classify(object()) == "recommendation"
    assert classifier.calls == 3
    assert delays == pytest.approx([0.1, 0.2])


def test_retries_transient_failure_then_succeeds():
    classifier = FlakyClassifier()
    retrying = RetryingClassifier(
        classifier,
        max_attempts=2,
        base_delay_seconds=0.0,
        sleep=lambda _: None,
    )

    result = retrying.classify(make_ticket())

    assert result.category == "billing"
    assert classifier.calls == 2


def test_gives_up_after_max_attempts():
    classifier = AlwaysFailingClassifier()
    retrying = RetryingClassifier(
        classifier,
        max_attempts=3,
        base_delay_seconds=0.0,
        sleep=lambda _: None,
    )

    with pytest.raises(TransientProviderError):
        retrying.classify(make_ticket())

    assert classifier.calls == 3


def test_permanent_error_is_not_retried():
    classifier = SequenceClassifier(
        [
            PermanentProviderError("invalid credentials"),
            "unused",
        ]
    )
    retrying = RetryingClassifier(
        classifier,
        sleep=lambda _: pytest.fail("Should not sleep"),
    )

    with pytest.raises(PermanentProviderError):
        retrying.classify(object())

    assert classifier.calls == 1


def test_unexpected_error_is_not_retried():
    classifier = SequenceClassifier([RuntimeError("boom"), "unused"])
    retrying = RetryingClassifier(
        classifier,
        max_attempts=3,
        sleep=lambda _: pytest.fail("Should not sleep"),
    )

    with pytest.raises(RuntimeError):
        retrying.classify(object())

    assert classifier.calls == 1


def test_retry_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        RetryingClassifier(FlakyClassifier(), max_attempts=0)
    with pytest.raises(ValueError):
        RetryingClassifier(FlakyClassifier(), base_delay_seconds=-1)
    with pytest.raises(ValueError):
        RetryingClassifier(FlakyClassifier(), max_delay_seconds=-1)
    with pytest.raises(ValueError):
        RetryingClassifier(
            FlakyClassifier(),
            base_delay_seconds=2.0,
            max_delay_seconds=1.0,
        )


def test_circuit_opens_and_closes_after_successful_probe():
    now = [100.0]
    classifier = SequenceClassifier(
        [
            TransientProviderError("failure 1"),
            TransientProviderError("failure 2"),
            "recovered",
        ]
    )

    breaker = CircuitBreakerClassifier(
        classifier,
        failure_threshold=2,
        reset_timeout_seconds=10,
        clock=lambda: now[0],
    )

    for _ in range(2):
        with pytest.raises(TransientProviderError):
            breaker.classify(object())

    assert breaker.state == CircuitState.OPEN

    calls_before = classifier.calls
    with pytest.raises(CircuitOpenError):
        breaker.classify(object())
    assert classifier.calls == calls_before

    now[0] += 11
    assert breaker.classify(object()) == "recovered"
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0


def test_failed_probe_reopens_circuit():
    now = [0.0]
    classifier = SequenceClassifier(
        [
            TransientProviderError("open"),
            TransientProviderError("probe fails"),
        ]
    )
    breaker = CircuitBreakerClassifier(
        classifier,
        failure_threshold=1,
        reset_timeout_seconds=5,
        clock=lambda: now[0],
    )

    with pytest.raises(TransientProviderError):
        breaker.classify(object())
    assert breaker.state == CircuitState.OPEN

    now[0] += 6
    with pytest.raises(TransientProviderError):
        breaker.classify(object())

    assert breaker.state == CircuitState.OPEN
    assert breaker.opened_at == 6.0


def test_permanent_error_does_not_count_toward_threshold():
    classifier = SequenceClassifier(
        [
            PermanentProviderError("bad credentials"),
            PermanentProviderError("bad credentials"),
        ]
    )
    breaker = CircuitBreakerClassifier(
        classifier,
        failure_threshold=2,
        reset_timeout_seconds=5,
        clock=lambda: 0.0,
    )

    for _ in range(2):
        with pytest.raises(PermanentProviderError):
            breaker.classify(object())

    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0


def test_permanent_probe_failure_reopens_circuit():
    now = [0.0]
    classifier = SequenceClassifier(
        [
            TransientProviderError("open"),
            PermanentProviderError("still broken"),
        ]
    )
    breaker = CircuitBreakerClassifier(
        classifier,
        failure_threshold=1,
        reset_timeout_seconds=5,
        clock=lambda: now[0],
    )

    with pytest.raises(TransientProviderError):
        breaker.classify(object())
    now[0] += 6

    with pytest.raises(PermanentProviderError):
        breaker.classify(object())

    assert breaker.state == CircuitState.OPEN
    assert breaker.opened_at == 6.0


def test_half_open_allows_only_one_probe():
    now = [0.0]
    breaker_holder = {}

    class ReentrantClassifier:
        def __init__(self) -> None:
            self.calls = 0

        def classify(self, ticket):
            self.calls += 1
            if self.calls == 1:
                raise TransientProviderError("open me")
            # During the recovery probe, a second probe must be rejected.
            with pytest.raises(CircuitOpenError):
                breaker_holder["breaker"].classify(object())
            return "recovered"

    classifier = ReentrantClassifier()
    breaker = CircuitBreakerClassifier(
        classifier,
        failure_threshold=1,
        reset_timeout_seconds=5,
        clock=lambda: now[0],
    )
    breaker_holder["breaker"] = breaker

    with pytest.raises(TransientProviderError):
        breaker.classify(object())
    assert breaker.state == CircuitState.OPEN

    now[0] += 6
    assert breaker.classify(object()) == "recovered"
    assert breaker.state == CircuitState.CLOSED


def test_circuit_breaker_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        CircuitBreakerClassifier(FlakyClassifier(), failure_threshold=0)
    with pytest.raises(ValueError):
        CircuitBreakerClassifier(FlakyClassifier(), reset_timeout_seconds=0)
    with pytest.raises(ValueError):
        CircuitBreakerClassifier(FlakyClassifier(), reset_timeout_seconds=-1)


def test_breaker_counts_one_failed_logical_request_not_each_retry():
    now = [0.0]
    classifier = AlwaysFailingClassifier()
    retrying = RetryingClassifier(
        classifier,
        max_attempts=3,
        base_delay_seconds=0.0,
        sleep=lambda _: None,
    )
    breaker = CircuitBreakerClassifier(
        retrying,
        failure_threshold=2,
        reset_timeout_seconds=5,
        clock=lambda: now[0],
    )

    # Each logical request exhausts the retry budget (3 provider calls) and
    # counts as exactly one breaker failure.
    with pytest.raises(TransientProviderError):
        breaker.classify(object())
    assert breaker.failure_count == 1

    with pytest.raises(TransientProviderError):
        breaker.classify(object())
    assert classifier.calls == 6
    assert breaker.state == CircuitState.OPEN
