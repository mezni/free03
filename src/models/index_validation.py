from pydantic import BaseModel, ConfigDict, Field


class IndexValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valid: bool

    document_count: int = Field(default=0, ge=0)
    chunk_count: int = Field(default=0, ge=0)
    embedding_count: int = Field(default=0, ge=0)

    expected_embedding_dimensions: int = Field(gt=0)
    invalid_embedding_count: int = Field(default=0, ge=0)

    duplicate_chunk_count: int = Field(default=0, ge=0)
    documents_without_chunks: int = Field(default=0, ge=0)
    chunks_without_embeddings: int = Field(default=0, ge=0)

    errors: list[str] = Field(default_factory=list)
