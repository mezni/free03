"""add llm usage tracking

Revision ID: 7f185a392a7f
Revises: e0fa455423de
Create Date: 2026-10-01 13:34:02.125308

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7f185a392a7f"
down_revision: str | None = "e0fa455423de"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create llm_usage."""
    op.create_table(
        "llm_usage",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "request_id", sa.String(length=100), nullable=True
        ),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column(
            "model_name", sa.String(length=200), nullable=False
        ),
        sa.Column("prompt_tokens", sa.Integer(), nullable=False),
        sa.Column("completion_tokens", sa.Integer(), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False),
        sa.Column("estimated_cost", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_llm_usage_model_name"),
        "llm_usage",
        ["model_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_llm_usage_request_id"),
        "llm_usage",
        ["request_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop llm_usage."""
    op.drop_index(
        op.f("ix_llm_usage_request_id"), table_name="llm_usage"
    )
    op.drop_index(
        op.f("ix_llm_usage_model_name"), table_name="llm_usage"
    )
    op.drop_table("llm_usage")