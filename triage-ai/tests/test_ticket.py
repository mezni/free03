import pytest
from pydantic import ValidationError

from triage_ai.models.ticket import SupportTicket


def test_create_support_ticket():
    ticket = SupportTicket(
        ticket_id="T-1001",
        customer_id="C-100",
        subject="Internet connection problem",
        description="My internet has been down since this morning.",
    )

    assert ticket.ticket_id == "T-1001"
    assert ticket.customer_id == "C-100"
    assert ticket.subject == "Internet connection problem"


def test_ticket_requires_subject():
    with pytest.raises(ValidationError):
        SupportTicket(
            ticket_id="T-1001",
            customer_id="C-100",
            subject="",
            description="My internet has been down.",
        )