from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RetrievalEvaluationCase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    case_id: str = Field(
        min_length=1,
        max_length=100,
    )

    query: str = Field(
        min_length=1,
    )

    relevant_chunk_ids: list[UUID] = Field(
        min_length=1,
    )


class RetrievalEvaluationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    case_id: str
    retrieved_chunk_ids: list[UUID]
    relevant_chunk_ids: list[UUID]