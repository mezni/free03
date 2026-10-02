from pathlib import Path

from pydantic import BaseModel

from triage_ai.data.loader import load_tickets
from triage_ai.models.ticket import SupportTicket


DATA_FILE = Path("data/tickets.json")


def test_load_tickets():
    tickets = load_tickets(DATA_FILE)

    assert len(tickets) == 10
    assert tickets[0].ticket_id == "T-1001"
    assert tickets[0].customer_id == "C-1001"


def test_loaded_objects_are_pydantic_models():
    tickets = load_tickets(DATA_FILE)

    assert isinstance(tickets[0], SupportTicket)
    assert isinstance(tickets[0], BaseModel)
    assert tickets[0].subject == "Internet connection is down"
    assert tickets[0].description
