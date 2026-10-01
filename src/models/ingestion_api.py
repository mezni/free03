from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import IngestionJobStatus


class CreateIngestionJobRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    source: str = Field(
        min_length=1,
        max_length=100,
    )

    input_path: str = Field(
        min_length=1,
        max_length=2000,
    )


class CreateIngestionJobResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    job_id: UUID
    status: IngestionJobStatus


class IngestionJobResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    job_id: UUID
    status: IngestionJobStatus
    run_id: UUID | None
    source: str
    input_path: str
    created_at: str | None
    started_at: str | None
    completed_at: str | None
    error_message: str | None