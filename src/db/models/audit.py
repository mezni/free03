from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class AuditEventDB(Base):
    """Persisted audit record.

    `created_at` uses a server default rather than a Python-side
    `datetime.utcnow`, matching `llm_usage`: the timestamp comes from
    one clock, and `datetime.utcnow()` is deprecated in Python 3.12+.
    """

    __tablename__ = "audit_events"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    request_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    actor: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    resource_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )