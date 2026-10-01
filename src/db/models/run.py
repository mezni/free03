from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.document_processing import DocumentProcessingDB


class IngestionRunDB(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    run_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    discovered_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    processed_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    skipped_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    processing_records: Mapped[list["DocumentProcessingDB"]] = relationship(
        "DocumentProcessingDB",
        back_populates="run",
    )
