from pydantic import BaseModel


class HistoricalTicket(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    body: str
    category: str
    resolution: str


class SimilarTicket(BaseModel):
    ticket_id: str
    subject: str
    category: str
    resolution: str
    score: int