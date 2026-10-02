from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.chunk import ChunkDB
    from src.db.models.document_processing import DocumentProcessingDB


class DocumentDB(Base):
    """Persistent representation of an ingested document."""

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source_uri: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    document_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )

    knowledge_base_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "knowledge_bases.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    knowledge_base = relationship(
        "KnowledgeBaseDB",
        back_populates="documents",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    chunks: Mapped[list["ChunkDB"]] = relationship(
        "ChunkDB",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    processing_records: Mapped[list["DocumentProcessingDB"]] = relationship(
        "DocumentProcessingDB",
        back_populates="document",
    )
