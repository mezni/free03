from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import Priority, Recommendation, Ticket
from ticket_triage.evaluation import (
    EvaluationExample,
    evaluate_classifier,
)


def test_evaluation_measures_field_accuracy():
    ticket = Ticket(
        ticket_id="T-401",
        subject="Charged twice",
        description="I was charged twice for one order.",
    )
    expected = Recommendation(
        category="billing",
        priority=Priority.HIGH,
        destination="billing-team",
        rationale="Duplicate charge reported.",
    )

    report = evaluate_classifier(
        FakeClassifier(),
        [EvaluationExample(ticket=ticket, expected=expected)],
    )

    assert report.total == 1
    assert report.failed == 0
    assert report.category_accuracy == 1.0
    assert report.priority_accuracy == 1.0
    assert report.destination_accuracy == 1.0
    assert report.failure_rate == 0.0


def test_evaluation_counts_classifier_failures():
    class BrokenClassifier:
        def classify(self, ticket):
            raise RuntimeError("simulated failure")

    class UnknownClassifier:
        def classify(self, ticket):
            return Recommendation(
                category="general",
                priority=Priority.LOW,
                destination="general-support",
                rationale="No match.",
            )

    unknown_ticket = Ticket(
        ticket_id="T-402",
        subject="Filing taxes",
        description="How do I file taxes?",
    )
    expected = Recommendation(
        category="general",
        priority=Priority.LOW,
        destination="general-support",
        rationale="General inquiry.",
    )
    broken_ticket = Ticket(
        ticket_id="T-403",
        subject="Broken",
        description="This will raise.",
    )

    report = evaluate_classifier(
        BrokenClassifier(),
        [EvaluationExample(ticket=broken_ticket, expected=expected)],
    )
    assert report.total == 1
    assert report.failed == 1
    assert report.failure_rate == 1.0
    assert report.category_accuracy == 0.0

    report = evaluate_classifier(
        UnknownClassifier(),
        [EvaluationExample(ticket=unknown_ticket, expected=expected)],
    )
    assert report.total == 1
    assert report.failed == 0
    assert report.category_accuracy == 1.0