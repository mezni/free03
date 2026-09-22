from support_agent.agent import (
    SupportTicket,
    TicketCategory,
    TicketPriority,
    TriageResult,
)


def test_support_ticket():
    ticket = SupportTicket(
        ticket_id="T001",
        customer_id="C001",
        message="I cannot log into my account.",
    )

    assert ticket.ticket_id == "T001"
    assert ticket.customer_id == "C001"


def test_triage_result():
    result = TriageResult(
        category=TicketCategory.ACCOUNT,
        priority=TicketPriority.HIGH,
        reasoning="The customer cannot access their account.",
        response="Let's help you recover access to your account.",
    )

    assert result.category == TicketCategory.ACCOUNT
    assert result.priority == TicketPriority.HIGH


def test_valid_triage_result():
    result = TriageResult(
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        reasoning="The customer reports a duplicate charge.",
        response="We can help investigate the duplicate charge.",
    )

    assert result.category == TicketCategory.BILLING
    assert result.priority == TicketPriority.HIGH