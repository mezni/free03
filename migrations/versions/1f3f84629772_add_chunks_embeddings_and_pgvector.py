"""add chunks embeddings and pgvector

Revision ID: 1f3f84629772
Revises: 58229e17449f
Create Date: 2026-09-16 14:03:57.910018

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "1f3f84629772"
down_revision: str | Sequence[str] | None = "58229e17449f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "chunks",
        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
        ),
        sa.Column(
            "document_id",
            sa.UUID(),
            sa.ForeignKey(
                "documents.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "content_hash",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "start_char",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "end_char",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_chunks_document_id",
        "chunks",
        ["document_id"],
    )

    op.create_table(
        "embeddings",
        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
        ),
        sa.Column(
            "chunk_id",
            sa.UUID(),
            sa.ForeignKey(
                "chunks.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "model_name",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "dimensions",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "vector",
            Vector(8),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_embeddings_chunk_id",
        "embeddings",
        ["chunk_id"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_embeddings_chunk_id",
        table_name="embeddings",
    )

    op.drop_table("embeddings")

    op.drop_index(
        "ix_chunks_document_id",
        table_name="chunks",
    )

    op.drop_table("chunks")
