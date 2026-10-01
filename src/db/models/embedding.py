from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class EmbeddingDB(Base):
    """Persisted embedding for a document chunk."""

    __tablename__ = "embeddings"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    chunk_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("chunks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    dimensions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    vector: Mapped[list[float]] = mapped_column(
        Vector(8),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
