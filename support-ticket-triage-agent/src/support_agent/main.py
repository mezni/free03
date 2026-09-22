import json
import re

from support_agent.client import chat
from support_agent.data.loader import load_tickets
from support_agent.models.ticket import TriageResult
from support_agent.prompts import TRIAGE_SYSTEM_PROMPT


def _parse_json(raw_result: str) -> dict:
    text = raw_result.strip()

    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)

    data = json.loads(text)
    return data


def triage_ticket(ticket):
    user_message = f"""
Support ticket:

Ticket ID: {ticket.ticket_id}
Customer ID: {ticket.customer_id}

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

    raw_result = chat(
        messages,
        system=TRIAGE_SYSTEM_PROMPT,
    )

    data = _parse_json(raw_result)

    return TriageResult.model_validate(data)


def main():
    tickets = load_tickets("data/tickets/tickets.json")

    for ticket in tickets:
        print("=" * 60)
        print(f"Ticket: {ticket.ticket_id}")
        print(f"Subject: {ticket.subject}")

        result = triage_ticket(ticket)

        print(f"Category: {result.category}")
        print(f"Urgency: {result.urgency}")
        print(f"Response: {result.response}")


if __name__ == "__main__":
    main()