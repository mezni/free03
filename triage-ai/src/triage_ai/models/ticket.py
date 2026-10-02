from pydantic import BaseModel, Field


class SupportTicket(BaseModel):
    ticket_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    description: str = Field(min_length=1)