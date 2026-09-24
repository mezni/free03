from typing import Literal

from pydantic import BaseModel


class CreateTicketInput(BaseModel):
    customer_id: str
    subject: str
    description: str
    priority: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]


class CreateTicketResult(BaseModel):
    ticket_id: str
    status: Literal["created"]