from typing import Literal

from pydantic import BaseModel


class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    body: str


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