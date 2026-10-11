from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import Priority, Ticket


def test_fake_classifier_identifies_billing_ticket():
    classifier = FakeClassifier()
    ticket = Ticket(
        ticket_id="T-100",
        subject="Charged twice",
        description="I see two charges on my account.",
    )
    result = classifier.classify(ticket)
    assert result.category == "billing"
    assert result.priority == Priority.HIGH
    assert result.destination == "billing-team"


def test_fake_classifier_handles_general_ticket():
    classifier = FakeClassifier()
    ticket = Ticket(
        ticket_id="T-101",
        subject="General question",
        description="I have a question about your service.",
    )
    result = classifier.classify(ticket)
    assert result.category == "general"
    assert result.destination == "general-support"
