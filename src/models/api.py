from pydantic import BaseModel, ConfigDict, Field

from src.models.rag import Citation


class RAGQueryRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    query: str = Field(
        min_length=1,
        max_length=5000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class RAGQueryResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    query: str
    answer: str
    citations: list[Citation]
    model_name: str
    retrieved_count: int
