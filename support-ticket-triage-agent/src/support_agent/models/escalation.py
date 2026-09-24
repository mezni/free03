from typing import Literal

from pydantic import BaseModel


class EscalateToHumanInput(BaseModel):
    ticket_id: str
    reason: str
    priority: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]


class EscalateToHumanResult(BaseModel):
    escalation_id: str
    ticket_id: str
    status: Literal["escalated"]