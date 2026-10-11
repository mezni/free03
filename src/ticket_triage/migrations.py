"""Additive, idempotent schema migrations for the SQLite database.

There is no migration-version table. Every statement is written so it can be
re-applied safely, which means an interrupted migration is retried on the next
startup instead of leaving a half-applied schema. Migrations never rewrite or
drop existing rows.
"""

import sqlite3


def apply_case_schema(connection: sqlite3.Connection) -> None:
    """Create ``triage_cases`` and add the Day 23 ``revision`` column."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS triage_cases (
            case_id TEXT PRIMARY KEY,
            revision INTEGER NOT NULL DEFAULT 0,
            payload TEXT NOT NULL
        )
        """
    )
    _add_revision_column_if_missing(connection)


def _add_revision_column_if_missing(connection: sqlite3.Connection) -> None:
    """Add ``revision`` to databases created before Day 23.

    ``CREATE TABLE IF NOT EXISTS`` never alters an existing table, so older
    databases need an explicit migration.
    """
    columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(triage_cases)")
    }
    if "revision" not in columns:
        connection.execute(
            "ALTER TABLE triage_cases ADD COLUMN revision INTEGER NOT NULL DEFAULT 0"
        )


def apply_routing_operations_schema(connection: sqlite3.Connection) -> None:
    """Create the Day 24 ``routing_operations`` table.

    The ``idempotency_key`` unique constraint stops the application from
    creating two operations for the same intended effect. The foreign key ties
    each operation to a stored case; foreign-key enforcement is enabled per
    connection by the repositories.
    """
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS routing_operations (
            operation_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            approval_decision_id TEXT NOT NULL,
            recommendation_version INTEGER NOT NULL,
            idempotency_key TEXT NOT NULL UNIQUE,
            ticket_id TEXT NOT NULL,
            destination TEXT NOT NULL,
            status TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            external_reference TEXT,
            last_error_code TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES triage_cases (case_id)
        )
        """
    )


def apply_all(connection: sqlite3.Connection) -> None:
    """Apply every migration in dependency order."""
    apply_case_schema(connection)
    apply_routing_operations_schema(connection)
