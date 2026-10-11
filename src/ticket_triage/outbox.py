"""Transactional outbox storage.

The outbox records events that describe work still to be dispatched. An event is
data, not executable code: it names an ``event_type`` and carries a JSON payload
that the dispatcher translates into a job.

The critical guarantee comes from writing the event and the business change in
one database transaction. ``add_event`` opens its own connection and is fine for
standalone inserts, but atomicity requires the caller-owned
``insert_event_in_transaction`` helper, which writes on a connection the caller
already controls (for example, the case repository's).
"""

import json
import sqlite3
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from ticket_triage.migrations import apply_outbox_schema


@dataclass(frozen=True)
class OutboxEvent:
    event_id: str
    event_type: str
    payload: dict
    attempts: int


def encode_payload(payload: dict) -> str:
    """Canonicalize a payload so identical requests encode identically."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def insert_event_in_transaction(
    connection: sqlite3.Connection,
    event_id: str,
    event_type: str,
    payload: dict,
) -> None:
    """Insert an outbox event using a caller-owned connection.

    This helper deliberately does not open a connection or commit. The caller
    owns the transaction, which is what makes the event atomic with the
    business write it accompanies.
    """
    connection.execute(
        """
        INSERT INTO outbox_events (
            event_id, event_type, payload, created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (event_id, event_type, encode_payload(payload), time.time()),
    )


class SQLiteOutbox:
    """Persist outbox events in a SQLite database."""

    def __init__(self, database_path: str):
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            apply_outbox_schema(connection)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """Open a connection, commit on success, and always close it."""
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def add_event(
        self,
        event_id: str,
        event_type: str,
        payload: dict,
    ) -> None:
        """Record an event, treating an identical re-submission as a no-op.

        The event ID is the idempotency key: the same ID with the same type and
        payload does not create a second event, while the same ID with different
        content is rejected.
        """
        if not event_id.strip() or not event_type.strip():
            raise ValueError("Event ID and type are required.")

        encoded = encode_payload(payload)

        with self._connect() as connection:
            existing = connection.execute(
                """
                SELECT event_type, payload
                FROM outbox_events WHERE event_id = ?
                """,
                (event_id,),
            ).fetchone()

            if existing is not None:
                if (
                    existing["event_type"] == event_type
                    and existing["payload"] == encoded
                ):
                    return
                raise ValueError("Event ID already exists with different content.")

            connection.execute(
                """
                INSERT INTO outbox_events (
                    event_id, event_type, payload, created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (event_id, event_type, encoded, time.time()),
            )

    def pending_events(self, limit: int = 100) -> list[OutboxEvent]:
        if limit < 1:
            raise ValueError("limit must be positive.")

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT event_id, event_type, payload, attempts
                FROM outbox_events
                WHERE status = 'pending'
                ORDER BY created_at, event_id
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            OutboxEvent(
                event_id=row["event_id"],
                event_type=row["event_type"],
                payload=json.loads(row["payload"]),
                attempts=row["attempts"],
            )
            for row in rows
        ]

    def mark_published(self, event_id: str) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE outbox_events
                SET status = 'published',
                    attempts = attempts + 1,
                    published_at = ?
                WHERE event_id = ? AND status = 'pending'
                """,
                (time.time(), event_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Event is not pending.")

    def record_dispatch_failure(self, event_id: str) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE outbox_events
                SET attempts = attempts + 1
                WHERE event_id = ? AND status = 'pending'
                """,
                (event_id,),
            )
            if cursor.rowcount != 1:
                raise ValueError("Event is not pending.")
