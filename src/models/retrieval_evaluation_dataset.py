from pydantic import BaseModel, ConfigDict, Field

from src.models.retrieval_evaluation import RetrievalEvaluationCase


class RetrievalEvaluationDataset(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    version: int = Field(ge=1)
    cases: list[RetrievalEvaluationCase] = Field(min_length=1)
