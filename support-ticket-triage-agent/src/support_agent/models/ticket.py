from typing import Literal

from pydantic import BaseModel


class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    body: str


class TicketExtraction(BaseModel):
    customer_id: str | None

    product: Literal[
        "internet",
        "mobile",
        "billing",
        "account",
        "shipping",
        "other",
    ]

    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
        "frustrated",
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]


class TriageResult(BaseModel):
    category: Literal[
        "billing",
        "technical_support",
        "account",
        "shipping",
        "security",
        "other",
    ]

    urgency: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]

    response: str