from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.document import DocumentDB
    from src.db.models.run import IngestionRunDB


class DocumentProcessingDB(Base):
    __tablename__ = "document_processing"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    run_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "ingestion_runs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    document_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    source_uri: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    operation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    run: Mapped["IngestionRunDB"] = relationship(
        "IngestionRunDB",
        back_populates="processing_records",
    )

    document: Mapped["DocumentDB | None"] = relationship(
        "DocumentDB",
        back_populates="processing_records",
    )
