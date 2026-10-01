"""add chunk full text search

Revision ID: e0fa455423de
Revises: 209814ea8e64
Create Date: 2026-09-25 15:33:00.072451
"""

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e0fa455423de"
down_revision: str | None = "209814ea8e64"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE chunks
        ADD COLUMN search_vector tsvector
        """
    )

    op.execute(
        """
        UPDATE chunks
        SET search_vector =
            to_tsvector(
                'english',
                coalesce(content, '')
            )
        """
    )

    op.execute(
        """
        CREATE FUNCTION chunks_search_vector_update()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            NEW.search_vector :=
                to_tsvector(
                    'english',
                    coalesce(NEW.content, '')
                );

            RETURN NEW;
        END;
        $$;
        """
    )

    op.execute(
        """
        CREATE TRIGGER chunks_search_vector_trigger
        BEFORE INSERT OR UPDATE OF content
        ON chunks
        FOR EACH ROW
        EXECUTE FUNCTION chunks_search_vector_update();
        """
    )

    op.execute(
        """
        CREATE INDEX ix_chunks_search_vector
        ON chunks
        USING GIN(search_vector)
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS ix_chunks_search_vector
        """
    )

    op.execute(
        """
        DROP TRIGGER IF EXISTS chunks_search_vector_trigger
        ON chunks
        """
    )

    op.execute(
        """
        DROP FUNCTION IF EXISTS chunks_search_vector_update()
        """
    )

    op.execute(
        """
        ALTER TABLE chunks
        DROP COLUMN IF EXISTS search_vector
        """
    )
