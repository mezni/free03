from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.document import DocumentDB
    from src.db.models.index_version import IndexVersionDB


class ChunkDB(Base):
    """Persisted document chunk."""

    __tablename__ = "chunks"

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "index_version_id",
            "chunk_index",
            name="uq_chunks_document_version_index",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    document_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    index_version_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("index_versions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    start_char: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    end_char: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR,
        nullable=True,
    )

    document: Mapped["DocumentDB"] = relationship(
        "DocumentDB",
        back_populates="chunks",
    )

    index_version: Mapped["IndexVersionDB"] = relationship(
        "IndexVersionDB",
        back_populates="chunks",
    )
