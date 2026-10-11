import pytest

from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import Ticket
from ticket_triage.observability import InstrumentedClassifier


def test_instrumented_classifier_records_success():
    classifier = InstrumentedClassifier(FakeClassifier())
    ticket = Ticket(
        ticket_id="T-301",
        subject="Charged twice",
        description="I was charged twice.",
    )

    result = classifier.classify(ticket)

    assert result.category == "billing"
    assert classifier.metrics.total_calls == 1
    assert classifier.metrics.successful_calls == 1
    assert classifier.metrics.failed_calls == 0
    assert classifier.metrics.total_latency_ms >= 0


def test_instrumented_classifier_records_failure():
    class BrokenClassifier:
        def classify(self, ticket):
            raise RuntimeError("simulated failure")

    classifier = InstrumentedClassifier(BrokenClassifier())
    ticket = Ticket(
        ticket_id="T-302",
        subject="Test",
        description="Synthetic ticket.",
    )

    with pytest.raises(RuntimeError):
        classifier.classify(ticket)

    assert classifier.metrics.total_calls == 1
    assert classifier.metrics.successful_calls == 0
    assert classifier.metrics.failed_calls == 1
    assert classifier.metrics.total_latency_ms >= 0
