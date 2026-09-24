import json
from pathlib import Path

from support_agent.models.tools import (
    CreateTicketInput,
    CreateTicketResult,
)


TICKET_STORE = Path("data/created_tickets.json")


def create_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str,
) -> dict:

    input_data = CreateTicketInput(
        customer_id=customer_id,
        subject=subject,
        description=description,
        priority=priority,
    )

    TICKET_STORE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if TICKET_STORE.exists():
        with TICKET_STORE.open(
            "r",
            encoding="utf-8",
        ) as file:
            tickets = json.load(file)
    else:
        tickets = []

    ticket_id = f"CT{len(tickets) + 1:03d}"

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": input_data.customer_id,
        "subject": input_data.subject,
        "description": input_data.description,
        "priority": input_data.priority,
        "status": "created",
    }

    tickets.append(ticket)

    with TICKET_STORE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            tickets,
            file,
            indent=2,
        )

    result = CreateTicketResult(
        ticket_id=ticket_id,
        status="created",
    )

    return result.model_dump()