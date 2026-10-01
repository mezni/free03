"""initial migration

Revision ID: b1e82f164fab
Revises:
Create Date: 2026-09-16 10:30:10.250130

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "b1e82f164fab"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
