from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import IngestionJobStatus


class IngestionJob(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    id: UUID | None = None

    status: IngestionJobStatus = IngestionJobStatus.PENDING

    run_id: UUID | None = None

    source: str = Field(
        min_length=1,
        max_length=100,
    )

    input_path: str = Field(
        min_length=1,
        max_length=2000,
    )

    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    error_message: str | None = Field(
        default=None,
        max_length=2000,
    )