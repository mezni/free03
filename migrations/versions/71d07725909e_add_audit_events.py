"""add audit events

Revision ID: 71d07725909e
Revises: 7f185a392a7f
Create Date: 2026-10-01 15:11:36.216620

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '71d07725909e'
down_revision: str | Sequence[str] | None = '7f185a392a7f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'audit_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('request_id', sa.String(length=100), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('actor', sa.String(length=200), nullable=True),
        sa.Column('resource_type', sa.String(length=100), nullable=True),
        sa.Column('resource_id', sa.String(length=200), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_audit_events_event_type'),
        'audit_events',
        ['event_type'],
        unique=False,
    )
    op.create_index(
        op.f('ix_audit_events_request_id'),
        'audit_events',
        ['request_id'],
        unique=False,
    )
    # Alembic's autogenerate reported `ix_chunks_search_vector` as
    # "removed" and offered to drop it. That index is created by
    # migration e0fa455423de and is absent from the ChunkDB model
    # because a GIN index over a generated TSVECTOR column cannot be
    # expressed in declarative metadata. Dropping it here would
    # silently disable keyword search for every deployed database, so
    # the diff is intentionally not applied.


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f('ix_audit_events_request_id'),
        table_name='audit_events',
    )
    op.drop_index(
        op.f('ix_audit_events_event_type'),
        table_name='audit_events',
    )
    op.drop_table('audit_events')