import json

from support_agent.client import chat
from support_agent.json_utils import parse_json
from support_agent.models.ticket import (
    TicketExtraction,
    TriageDecision,
)
from support_agent.prompts import TRIAGE_DECISION_SYSTEM_PROMPT


def decide_triage(
    extraction: TicketExtraction,
) -> TriageDecision:

    user_message = f"""
Decide how this support ticket should be handled.

Customer ID:
{extraction.customer_id}

Product:
{extraction.product}

Sentiment:
{extraction.sentiment}

Priority:
{extraction.priority}
"""

    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    raw_response = chat(
        messages,
        system=TRIAGE_DECISION_SYSTEM_PROMPT,
    )

    data = parse_json(raw_response)

    return TriageDecision.model_validate(data)