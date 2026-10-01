from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import IndexOperation, IndexVersionStatus


class IndexRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation: IndexOperation
    document_id: UUID | None = None
    index_version_id: UUID | None = None
    reason: str | None = Field(default=None, max_length=500)


class IndexVersion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID | None = None
    version_number: int = Field(ge=1)
    status: IndexVersionStatus
    embedding_model: str = Field(min_length=1, max_length=255)
    embedding_dimensions: int = Field(gt=0)
    created_at: datetime | None = None
    activated_at: datetime | None = None
