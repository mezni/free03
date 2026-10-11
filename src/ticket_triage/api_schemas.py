from pydantic import BaseModel, ConfigDict, Field

from ticket_triage.domain import CaseStatus, Priority


class CreateCaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1, max_length=100)
    ticket_id: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1, max_length=20_000)


class RecommendationResponse(BaseModel):
    category: str
    priority: Priority
    destination: str
    rationale: str


class CaseResponse(BaseModel):
    case_id: str
    ticket_id: str
    status: CaseStatus
    recommendation: RecommendationResponse | None = None
    recommendation_version: int