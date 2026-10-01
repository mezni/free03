from pydantic import BaseModel, ConfigDict, Field

from src.models.retrieval import RetrievalResult


class MultiQueryResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    queries: list[str] = Field(min_length=1)

    results: list[RetrievalResult]