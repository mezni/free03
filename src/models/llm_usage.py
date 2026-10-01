from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LLMUsageRecord(BaseModel):
    """One LLM call: tokens consumed and estimated cost."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    id: UUID | None = None

    request_id: str | None = None

    provider: str = Field(
        min_length=1,
        max_length=100,
    )

    model_name: str = Field(
        min_length=1,
        max_length=200,
    )

    prompt_tokens: int = Field(
        default=0,
        ge=0,
    )

    completion_tokens: int = Field(
        default=0,
        ge=0,
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
    )

    estimated_cost: float = Field(
        default=0.0,
        ge=0,
    )

    currency: str = Field(
        default="USD",
        min_length=3,
        max_length=3,
    )

    created_at: datetime | None = None
