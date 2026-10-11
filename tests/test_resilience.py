import pytest

from ticket_triage.domain import Priority, Recommendation, Ticket
from ticket_triage.errors import TransientProviderError
from ticket_triage.resilience import RetryingClassifier


class FlakyClassifier:
    def __init__(self):
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
    def __init__(self):
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


def test_retries_transient_failure_then_succeeds():
    classifier = FlakyClassifier()
    retrying = RetryingClassifier(
        classifier,
        max_attempts=2,
        retry_delay_seconds=0.0,
    )

    result = retrying.classify(make_ticket())

    assert result.category == "billing"
    assert result.priority == Priority.HIGH
    assert classifier.calls == 2


def test_gives_up_after_max_attempts():
    classifier = AlwaysFailingClassifier()
    retrying = RetryingClassifier(classifier, max_attempts=3)

    with pytest.raises(TransientProviderError):
        retrying.classify(make_ticket())

    assert classifier.calls == 3


def test_does_not_retry_non_transient_errors():
    class BrokenClassifier:
        def __init__(self):
            self.calls = 0

        def classify(self, ticket):
            self.calls += 1
            raise RuntimeError("boom")

    classifier = BrokenClassifier()
    retrying = RetryingClassifier(classifier, max_attempts=3)

    with pytest.raises(RuntimeError):
        retrying.classify(make_ticket())

    assert classifier.calls == 1


def test_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        RetryingClassifier(FlakyClassifier(), max_attempts=0)
    with pytest.raises(ValueError):
        RetryingClassifier(FlakyClassifier(), retry_delay_seconds=-1)
