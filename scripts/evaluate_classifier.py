from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import Priority, Recommendation, Ticket
from ticket_triage.evaluation import (
    EvaluationExample,
    evaluate_classifier,
)

examples = [
    EvaluationExample(
        ticket=Ticket(
            ticket_id="E-001",
            subject="Charged twice",
            description="Two charges appeared for one order.",
        ),
        expected=Recommendation(
            category="billing",
            priority=Priority.HIGH,
            destination="billing-team",
            rationale="Duplicate payment.",
        ),
    ),
    EvaluationExample(
        ticket=Ticket(
            ticket_id="E-002",
            subject="Cannot log in",
            description="I cannot access my account.",
        ),
        expected=Recommendation(
            category="account",
            priority=Priority.MEDIUM,
            destination="account-support",
            rationale="Account access problem.",
        ),
    ),
    EvaluationExample(
        ticket=Ticket(
            ticket_id="E-003",
            subject="General question",
            description="I have a question about your service.",
        ),
        expected=Recommendation(
            category="general",
            priority=Priority.LOW,
            destination="general-support",
            rationale="General inquiry.",
        ),
    ),
]

report = evaluate_classifier(FakeClassifier(), examples)

print(f"Examples evaluated: {report.total}")
print(f"Failed calls: {report.failed}")
print(f"Failure rate: {report.failure_rate:.2%}")
print(f"Category accuracy: {report.category_accuracy:.2%}")
print(f"Priority accuracy: {report.priority_accuracy:.2%}")
print(f"Destination accuracy: {report.destination_accuracy:.2%}")