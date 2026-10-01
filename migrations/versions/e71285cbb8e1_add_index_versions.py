"""add index versions

Revision ID: e71285cbb8e1
Revises: 1f3f84629772
Create Date: 2026-09-16 16:23:37.624158

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e71285cbb8e1"
down_revision: str | Sequence[str] | None = "1f3f84629772"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "index_versions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("embedding_model", sa.String(length=255), nullable=False),
        sa.Column("embedding_dimensions", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.add_column(
        "chunks",
        sa.Column("index_version_id", sa.UUID(), nullable=False),
    )

    op.create_index(
        op.f("ix_chunks_index_version_id"),
        "chunks",
        ["index_version_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_chunks_index_version_id_index_versions",
        "chunks",
        "index_versions",
        ["index_version_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_chunks_index_version_id_index_versions",
        "chunks",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_chunks_index_version_id"),
        table_name="chunks",
    )

    op.drop_column("chunks", "index_version_id")

    op.drop_table("index_versions")
