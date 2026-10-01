from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import DocumentLifecycleStatus


class DocumentCreate(BaseModel):
    """Data required to create a document."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1, max_length=100)
    source_uri: str = Field(min_length=1)
    title: str | None = Field(default=None, max_length=500)
    document_type: str | None = Field(default=None, max_length=100)

    content_hash: str = Field(
        min_length=64,
        max_length=64,
        pattern=r"^[a-fA-F0-9]{64}$",
    )

    status: DocumentLifecycleStatus = DocumentLifecycleStatus.PENDING


class Document(BaseModel):
    """Application representation of a persisted document."""

    model_config = ConfigDict(extra="forbid")

    id: UUID | None = None

    source: str = Field(min_length=1, max_length=100)
    source_uri: str = Field(min_length=1)
    title: str | None = Field(default=None, max_length=500)
    document_type: str | None = Field(default=None, max_length=100)

    content_hash: str = Field(
        min_length=64,
        max_length=64,
        pattern=r"^[a-fA-F0-9]{64}$",
    )

    status: DocumentLifecycleStatus = DocumentLifecycleStatus.PENDING

    created_at: datetime | None = None
    updated_at: datetime | None = None
