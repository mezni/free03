import json

from support_agent.client import chat
from support_agent.guardrails import validate_extraction_output
from support_agent.models.ticket import SupportTicket
from support_agent.prompts import EXTRACTION_SYSTEM_PROMPT


def extract_ticket(
    ticket: SupportTicket,
):

    user_message = f"""
Extract information from this support ticket.

Ticket ID:
{ticket.ticket_id}

Customer ID:
{ticket.customer_id}

Subject:
{ticket.subject}

Message:
{ticket.body}
"""

    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    raw_response = chat(
        messages,
        system=EXTRACTION_SYSTEM_PROMPT,
    )

    return validate_extraction_output(
        raw_response,
    )