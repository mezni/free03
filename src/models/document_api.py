
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentListRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class DocumentSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID
    source: str
    source_uri: str
    title: str | None
    document_type: str | None
    status: str
    created_at: str | None
    updated_at: str | None


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    items: list[DocumentSummary]
    total: int


class DocumentDetailResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID
    source: str
    source_uri: str
    title: str | None
    document_type: str | None
    content_hash: str
    status: str
    created_at: str | None
    updated_at: str | None


class DocumentIngestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: Path


class DocumentIngestResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    run_id: str
    discovered_count: int
    processed_count: int
    skipped_count: int
    failed_count: int
    document_ids: list[str]
