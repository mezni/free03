from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import (
    DocumentProcessingOperation,
    DocumentProcessingStatus,
    IngestionRunStatus,
)


class IngestionRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID | None = None
    run_type: str = Field(min_length=1, max_length=50)
    status: IngestionRunStatus = IngestionRunStatus.RUNNING

    started_at: datetime | None = None
    completed_at: datetime | None = None

    discovered_count: int = Field(default=0, ge=0)
    processed_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    failed_count: int = Field(default=0, ge=0)

    error_message: str | None = Field(
        default=None,
        max_length=2000,
    )


class DocumentProcessingResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID | None = None
    run_id: UUID
    document_id: UUID | None = None

    source_uri: str = Field(min_length=1)
    operation: DocumentProcessingOperation
    status: DocumentProcessingStatus

    error_message: str | None = Field(
        default=None,
        max_length=2000,
    )
