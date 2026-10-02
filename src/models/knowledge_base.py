
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeBaseCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    name: str = Field(
        min_length=1,
        max_length=200,
    )

    slug: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )


class KnowledgeBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    id: UUID | None = None
    name: str
    slug: str
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
