from pydantic import BaseModel, ConfigDict, Field


class Citation(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    citation_id: str = Field(min_length=1)
    document_id: str
    chunk_id: str
    chunk_index: int = Field(ge=0)


class RAGResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    query: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    model_name: str
    retrieved_count: int = Field(ge=0)
