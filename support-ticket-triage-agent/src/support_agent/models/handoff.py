from pydantic import BaseModel


class ResearchRequest(BaseModel):
    ticket_id: str
    customer_id: str | None
    issue_summary: str
    category: str
    urgency: str
    product: str
    priority: str
    research_question: str


class ResearchResult(BaseModel):
    ticket_id: str
    findings: str
    similar_tickets: list["SimilarTicket"]


class SimilarTicket(BaseModel):
    ticket_id: str
    subject: str
    category: str
    resolution: str
    score: int