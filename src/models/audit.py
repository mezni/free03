from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditEvent(BaseModel):
    """A significant application action.

    Records *that* something happened, never the sensitive contents of
    what it happened to. Document text, credentials, and provider
    responses have no place here: an audit table is usually retained
    longer and read more widely than the data it describes.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    id: UUID | None = None

    request_id: str | None = None

    event_type: str = Field(
        min_length=1,
        max_length=100,
    )

    actor: str | None = Field(
        default=None,
        max_length=200,
    )

    resource_type: str | None = Field(
        default=None,
        max_length=100,
    )

    resource_id: str | None = Field(
        default=None,
        max_length=200,
    )

    created_at: datetime | None = None