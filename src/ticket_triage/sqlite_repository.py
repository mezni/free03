"""SQLite persistence adapter for triage cases.

The adapter implements the ``CaseRepository`` interface. It is an infrastructure
detail: only this module knows about SQL, JSON serialization, and revisions.

Concurrency model
-----------------
Each stored case carries a database-managed ``revision``. Updates use a
compare-and-swap statement (``save_if_revision``) that only succeeds when the
stored revision still matches the revision the caller read. Case creation uses a
plain ``INSERT`` so the primary-key constraint rejects duplicate case IDs under
concurrent execution.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from ticket_triage.domain import (
    ApprovalDecision,
    CaseStatus,
    DecisionType,
    Priority,
    Recommendation,
    Ticket,
    TriageCase,
)
from ticket_triage.errors import ConcurrentUpdateError, DuplicateCaseError
from ticket_triage.repositories import CaseRecord


def _recommendation_to_payload(
    recommendation: Recommendation | None,
) -> dict | None:
    if recommendation is None:
        return None
    return {
        "category": recommendation.category,
        "priority": recommendation.priority.value,
        "destination": recommendation.destination,
        "rationale": recommendation.rationale,
    }


def _approval_to_payload(approval: ApprovalDecision | None) -> dict | None:
    if approval is None:
        return None
    return {
        "decision_id": approval.decision_id,
        "case_id": approval.case_id,
        "recommendation_version": approval.recommendation_version,
        "actor_id": approval.actor_id,
        "decision": approval.decision.value,
        "decided_at": approval.decided_at.isoformat(),
        "comment": approval.comment,
    }


def case_to_payload(case: TriageCase) -> dict:
    """Serialize a case to a JSON-compatible dictionary."""
    return {
        "case_id": case.case_id,
        "ticket": {
            "ticket_id": case.ticket.ticket_id,
            "subject": case.ticket.subject,
            "description": case.ticket.description,
        },
        "status": case.status.value,
        "recommendation": _recommendation_to_payload(case.recommendation),
        "recommendation_version": case.recommendation_version,
        "approval_decision": _approval_to_payload(case.approval_decision),
    }


def case_from_payload(payload: dict) -> TriageCase:
    """Rebuild a case from the payload produced by ``case_to_payload``."""
    ticket_payload = payload["ticket"]
    recommendation_payload = payload.get("recommendation")
    approval_payload = payload.get("approval_decision")

    recommendation = None
    if recommendation_payload is not None:
        recommendation = Recommendation(
            category=recommendation_payload["category"],
            priority=Priority(recommendation_payload["priority"]),
            destination=recommendation_payload["destination"],
            rationale=recommendation_payload["rationale"],
        )

    approval = None
    if approval_payload is not None:
        approval = ApprovalDecision(
            decision_id=approval_payload["decision_id"],
            case_id=approval_payload["case_id"],
            recommendation_version=approval_payload["recommendation_version"],
            actor_id=approval_payload["actor_id"],
            decision=DecisionType(approval_payload["decision"]),
            decided_at=datetime.fromisoformat(approval_payload["decided_at"]),
            comment=approval_payload.get("comment"),
        )

    return TriageCase(
        case_id=payload["case_id"],
        ticket=Ticket(
            ticket_id=ticket_payload["ticket_id"],
            subject=ticket_payload["subject"],
            description=ticket_payload["description"],
        ),
        status=CaseStatus(payload["status"]),
        recommendation=recommendation,
        recommendation_version=payload.get("recommendation_version", 0),
        approval_decision=approval,
    )


class SQLiteCaseRepository:
    """Store triage cases in a SQLite database."""

    def __init__(self, database_path: str, *, timeout: float = 5.0) -> None:
        self.database_path = database_path
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(
            database_path,
            timeout=timeout,
            check_same_thread=False,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        if database_path != ":memory:":
            self._connection.execute("PRAGMA journal_mode = WAL")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS triage_cases (
                    case_id TEXT PRIMARY KEY,
                    revision INTEGER NOT NULL DEFAULT 0,
                    payload TEXT NOT NULL
                )
                """
            )
            self._migrate_revision_column()

    def _migrate_revision_column(self) -> None:
        """Add the revision column to databases created before Day 23.

        ``CREATE TABLE IF NOT EXISTS`` never alters an existing table, so older
        databases need an explicit migration.
        """
        columns = {
            row["name"]
            for row in self._connection.execute("PRAGMA table_info(triage_cases)")
        }
        if "revision" not in columns:
            self._connection.execute(
                "ALTER TABLE triage_cases "
                "ADD COLUMN revision INTEGER NOT NULL DEFAULT 0"
            )

    def create(self, case: TriageCase) -> None:
        """Insert a new case, raising ``DuplicateCaseError`` on conflict."""
        payload = json.dumps(case_to_payload(case))
        try:
            with self._connection:
                self._connection.execute(
                    "INSERT INTO triage_cases (case_id, revision, payload) "
                    "VALUES (?, 0, ?)",
                    (case.case_id, payload),
                )
        except sqlite3.IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc) or "PRIMARY KEY" in str(exc):
                raise DuplicateCaseError(
                    f"Case {case.case_id} already exists."
                ) from exc
            raise

    def save(self, case: TriageCase) -> None:
        payload = json.dumps(case_to_payload(case))
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO triage_cases (case_id, revision, payload)
                VALUES (?, 0, ?)
                ON CONFLICT(case_id) DO UPDATE SET
                    payload = excluded.payload,
                    revision = triage_cases.revision + 1
                """,
                (case.case_id, payload),
            )

    def get(self, case_id: str) -> TriageCase | None:
        record = self.get_with_revision(case_id)
        return None if record is None else record.case

    def get_with_revision(self, case_id: str) -> CaseRecord | None:
        row = self._connection.execute(
            "SELECT revision, payload FROM triage_cases WHERE case_id = ?",
            (case_id,),
        ).fetchone()
        if row is None:
            return None
        return CaseRecord(
            case=case_from_payload(json.loads(row["payload"])),
            revision=row["revision"],
        )

    def save_if_revision(self, case: TriageCase, expected_revision: int) -> None:
        payload = json.dumps(case_to_payload(case))
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE triage_cases
                SET payload = ?,
                    revision = revision + 1
                WHERE case_id = ?
                  AND revision = ?
                """,
                (payload, case.case_id, expected_revision),
            )
        if cursor.rowcount != 1:
            raise ConcurrentUpdateError("The case changed; reload before retrying.")

    def health_check(self) -> bool:
        try:
            self._connection.execute("SELECT 1").fetchone()
            return True
        except sqlite3.Error:
            return False
