import json
import os
from enum import Enum

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel


class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    message: str


class TicketCategory(str, Enum):
    ACCOUNT = "account"
    BILLING = "billing"
    TECHNICAL = "technical"
    PRODUCT = "product"
    SHIPPING = "shipping"
    OTHER = "other"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TriageResult(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    reasoning: str
    response: str


load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv(
    "ANTHROPIC_MODEL",
    "claude-sonnet-4-6",
)

if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not configured.")


TRIAGE_SYSTEM_PROMPT = """
You are a customer support triage assistant.

Your job is to analyze a customer support ticket.

Determine:
1. The most appropriate category.
2. The priority.
3. A concise explanation of your reasoning.
4. A helpful draft response to the customer.

Categories:
- account
- billing
- technical
- product
- shipping
- other

Priorities:
- low
- medium
- high
- urgent

Do not claim that you performed an action that you cannot perform.
Do not invent information that is not present in the ticket.

Return your answer as JSON with these fields:

{
  "category": "...",
  "priority": "...",
  "reasoning": "...",
  "response": "..."
}
"""


client = Anthropic(api_key=ANTHROPIC_API_KEY)


def ask_llm(system_prompt: str, user_message: str) -> str:
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
    )

    return response.content[0].text


def _extract_json(raw_response: str) -> dict:
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(cleaned[start : end + 1])

    raise ValueError(f"Could not parse LLM response as JSON: {raw_response!r}")


def triage_ticket(ticket: SupportTicket) -> TriageResult:
    raw_response = ask_llm(
        system_prompt=TRIAGE_SYSTEM_PROMPT,
        user_message=ticket.message,
    )

    data = _extract_json(raw_response)

    return TriageResult.model_validate(data)