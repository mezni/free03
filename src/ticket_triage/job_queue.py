"""A small persistent SQLite-backed job queue.

This is a teaching implementation, not a production queue. It exists so the
core queue mechanics—persistence, claiming, leases, retries, and
acknowledgment—can be learned without introducing Redis, Celery, or another
external service.

Important distinction: ``async``/``await`` improves asynchronous I/O, but it is
not a durable job queue. By itself it does not make work survive a process
crash. The same is true of FastAPI's ``BackgroundTasks``: convenient for
lightweight work, but not a durable queue for critical processing.

Delivery is **at-least-once**. A job can be claimed and executed more than
once—for example, when a worker performs the work and then crashes before
recording success, and its lease expires. Handlers must therefore be idempotent.
"""

import json
import sqlite3
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Job:
    job_id: str
    job_type: str
    payload: dict
    status: str
    attempts: int


class SQLiteJobQueue:
    """A small persistent queue for learning and local development."""

    def __init__(self, database_path: str):
        self.database_path = database_path
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (
                        status IN ('queued', 'running', 'succeeded', 'failed')
                    ),
                    attempts INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL,
                    available_at REAL NOT NULL,
                    locked_until REAL,
                    last_error TEXT
                )
                """
            )

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

    def enqueue(
        self,
        job_id: str,
        job_type: str,
        payload: dict,
        *,
        max_attempts: int = 3,
    ) -> None:
        if not job_id.strip() or not job_type.strip():
            raise ValueError("Job ID and type are required.")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO jobs (
                    job_id, job_type, payload, status,
                    attempts, max_attempts, available_at
                )
                VALUES (?, ?, ?, 'queued', 0, ?, ?)
                """,
                (
                    job_id,
                    job_type,
                    json.dumps(payload),
                    max_attempts,
                    # A fresh job is eligible immediately. Future availability
                    # is scheduled by fail() using an explicit clock so the
                    # queue can be exercised with a synthetic ``now`` in tests.
                    0.0,
                ),
            )

    def claim_next(
        self, *, now: float | None = None, lease_seconds: int = 60
    ) -> Job | None:
        if lease_seconds < 1:
            raise ValueError("lease_seconds must be positive.")

        now = time.time() if now is None else now

        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")

            # Jobs whose final attempt expired cannot remain stuck running.
            connection.execute(
                """
                UPDATE jobs
                SET status = 'failed', locked_until = NULL,
                    last_error = COALESCE(last_error, 'Worker lease expired')
                WHERE attempts >= max_attempts
                  AND (
                    status = 'queued'
                    OR (status = 'running' AND locked_until <= ?)
                  )
                """,
                (now,),
            )

            row = connection.execute(
                """
                SELECT * FROM jobs
                WHERE attempts < max_attempts
                  AND available_at <= ?
                  AND (
                    status = 'queued'
                    OR (status = 'running' AND locked_until <= ?)
                  )
                ORDER BY available_at, job_id
                LIMIT 1
                """,
                (now, now),
            ).fetchone()

            if row is None:
                return None

            connection.execute(
                """
                UPDATE jobs
                SET status = 'running',
                    attempts = attempts + 1,
                    locked_until = ?
                WHERE job_id = ?
                """,
                (now + lease_seconds, row["job_id"]),
            )

            return Job(
                job_id=row["job_id"],
                job_type=row["job_type"],
                payload=json.loads(row["payload"]),
                status="running",
                attempts=row["attempts"] + 1,
            )

    def complete(self, job_id: str) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE jobs
                SET status = 'succeeded', locked_until = NULL,
                    last_error = NULL
                WHERE job_id = ? AND status = 'running'
                """,
                (job_id,),
            )
            if cursor.rowcount != 1:
                raise ValueError("Job is not currently running.")

    def fail(
        self,
        job: Job,
        error: str,
        *,
        retry_delay_seconds: int = 5,
        now: float | None = None,
    ) -> None:
        if retry_delay_seconds < 0:
            raise ValueError("Retry delay cannot be negative.")

        now = time.time() if now is None else now
        safe_error = error[:500]

        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE jobs
                SET status = ?,
                    available_at = ?,
                    locked_until = NULL,
                    last_error = ?
                WHERE job_id = ? AND status = 'running'
                """,
                (
                    "failed"
                    if job.attempts >= self._max_attempts(job.job_id)
                    else "queued",
                    now + retry_delay_seconds,
                    safe_error,
                    job.job_id,
                ),
            )
            if cursor.rowcount != 1:
                raise ValueError("Job is not currently running.")

    def _max_attempts(self, job_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT max_attempts FROM jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
        if row is None:
            raise ValueError("Unknown job.")
        return row["max_attempts"]

    def get_status(self, job_id: str) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT status FROM jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
        return row["status"] if row else None


def process_one(
    queue: SQLiteJobQueue,
    handler: Callable[[Job], None],
    *,
    now: float | None = None,
) -> bool:
    """Process at most one available job. Return whether one was claimed.

    A handler that raises is treated as a failed attempt: the job is requeued
    for retry, or marked failed once its attempts are exhausted. Because a
    worker can crash between performing work and recording success, handlers
    must be idempotent.
    """
    job = queue.claim_next(now=now)
    if job is None:
        return False

    try:
        handler(job)
    except Exception as exc:
        queue.fail(job, type(exc).__name__, now=now)
    else:
        queue.complete(job.job_id)

    return True
