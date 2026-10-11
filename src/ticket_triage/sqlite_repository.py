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
from datetime import UTC, datetime
from pathlib import Path

from ticket_triage.domain import (
    ApprovalDecision,
    CaseStatus,
    DecisionType,
    Priority,
    Recommendation,
    RoutingOperation,
    RoutingStatus,
    Ticket,
    TriageCase,
)
from ticket_triage.errors import ConcurrentUpdateError, DuplicateCaseError
from ticket_triage.migrations import (
    apply_case_schema,
    apply_outbox_schema,
    apply_routing_operations_schema,
)
from ticket_triage.outbox import insert_event_in_transaction
from ticket_triage.repositories import CaseRecord


def _connect(database_path: str, timeout: float) -> sqlite3.Connection:
    """Open a connection with the settings every adapter relies on."""
    if database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(
        database_path,
        timeout=timeout,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    if database_path != ":memory:":
        connection.execute("PRAGMA journal_mode = WAL")
    return connection


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
        self._connection = _connect(database_path, timeout)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            apply_case_schema(self._connection)
            apply_outbox_schema(self._connection)

    def close(self) -> None:
        """Release the underlying connection."""
        self._connection.close()

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

    def create_case_with_classification_event(self, case: TriageCase) -> None:
        """Insert a case and its classification event in one transaction.

        Both rows commit together or neither does. The event is written on the
        repository's connection through ``insert_event_in_transaction`` so no
        second connection can break the atomicity. ``with self._connection``
        commits on success and rolls back if any statement raises.
        """
        payload = json.dumps(case_to_payload(case))
        try:
            with self._connection:
                self._connection.execute(
                    "INSERT INTO triage_cases (case_id, revision, payload) "
                    "VALUES (?, 0, ?)",
                    (case.case_id, payload),
                )
                insert_event_in_transaction(
                    self._connection,
                    event_id=f"classify:{case.case_id}",
                    event_type="classification_requested",
                    payload={"case_id": case.case_id},
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


def _routing_row_to_operation(row: sqlite3.Row) -> RoutingOperation:
    return RoutingOperation(
        operation_id=row["operation_id"],
        case_id=row["case_id"],
        approval_decision_id=row["approval_decision_id"],
        recommendation_version=row["recommendation_version"],
        idempotency_key=row["idempotency_key"],
        ticket_id=row["ticket_id"],
        destination=row["destination"],
        status=RoutingStatus(row["status"]),
        attempts=row["attempts"],
        external_reference=row["external_reference"],
        last_error_code=row["last_error_code"],
    )


class SQLiteRoutingOperationRepository:
    """Persist routing operations so intent survives a process restart."""

    def __init__(self, database_path: str, *, timeout: float = 5.0) -> None:
        self.database_path = database_path
        self._connection = _connect(database_path, timeout)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            apply_case_schema(self._connection)
            apply_routing_operations_schema(self._connection)

    def close(self) -> None:
        """Release the underlying connection."""
        self._connection.close()

    def create_or_get(
        self,
        operation: RoutingOperation,
    ) -> tuple[RoutingOperation, bool]:
        """Insert the operation, or return the existing one for its key.

        Returns ``(operation, created)``. The unique ``idempotency_key`` makes
        this safe under concurrent retries: exactly one caller creates the row.
        """
        timestamp = datetime.now(UTC).isoformat()
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO routing_operations (
                        operation_id,
                        case_id,
                        approval_decision_id,
                        recommendation_version,
                        idempotency_key,
                        ticket_id,
                        destination,
                        status,
                        attempts,
                        external_reference,
                        last_error_code,
                        created_at,
                        updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        operation.operation_id,
                        operation.case_id,
                        operation.approval_decision_id,
                        operation.recommendation_version,
                        operation.idempotency_key,
                        operation.ticket_id,
                        operation.destination,
                        operation.status.value,
                        operation.attempts,
                        operation.external_reference,
                        operation.last_error_code,
                        timestamp,
                        timestamp,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc) or "PRIMARY KEY" in str(exc):
                existing = self.get_by_idempotency_key(operation.idempotency_key)
                if existing is not None:
                    return existing, False
            raise
        stored = self.get(operation.operation_id)
        if stored is None:
            raise RuntimeError("Routing operation vanished after insert.")
        return stored, True

    def get(self, operation_id: str) -> RoutingOperation | None:
        row = self._connection.execute(
            "SELECT * FROM routing_operations WHERE operation_id = ?",
            (operation_id,),
        ).fetchone()
        return None if row is None else _routing_row_to_operation(row)

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> RoutingOperation | None:
        row = self._connection.execute(
            "SELECT * FROM routing_operations WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        return None if row is None else _routing_row_to_operation(row)

    def list_unresolved(self) -> list[RoutingOperation]:
        """Return operations that have not reached a confirmed outcome.

        This is the recovery set: pending, in-progress, unknown, and
        reconciliation-required operations are all discovered on restart.
        """
        unresolved = {
            RoutingStatus.PENDING.value,
            RoutingStatus.IN_PROGRESS.value,
            RoutingStatus.OUTCOME_UNKNOWN.value,
            RoutingStatus.RECONCILIATION_REQUIRED.value,
        }
        rows = self._connection.execute(
            "SELECT * FROM routing_operations WHERE status IN (?, ?, ?, ?) "
            "ORDER BY created_at",
            tuple(sorted(unresolved)),
        ).fetchall()
        return [_routing_row_to_operation(row) for row in rows]

    def _update(
        self,
        operation_id: str,
        *,
        status: RoutingStatus,
        external_reference: str | None = None,
        last_error_code: str | None = None,
        increment_attempts: bool = False,
    ) -> None:
        timestamp = datetime.now(UTC).isoformat()
        attempts_expression = "attempts + 1" if increment_attempts else "attempts"
        with self._connection:
            cursor = self._connection.execute(
                f"""
                UPDATE routing_operations
                SET status = ?,
                    external_reference = ?,
                    last_error_code = ?,
                    attempts = {attempts_expression},
                    updated_at = ?
                WHERE operation_id = ?
                """,
                (
                    status.value,
                    external_reference,
                    last_error_code,
                    timestamp,
                    operation_id,
                ),
            )
        if cursor.rowcount != 1:
            raise LookupError(f"Unknown routing operation {operation_id}.")

    def mark_in_progress(self, operation_id: str) -> None:
        self._update(
            operation_id,
            status=RoutingStatus.IN_PROGRESS,
            increment_attempts=True,
        )

    def mark_succeeded(
        self,
        operation_id: str,
        *,
        external_reference: str,
    ) -> None:
        self._update(
            operation_id,
            status=RoutingStatus.SUCCEEDED,
            external_reference=external_reference,
        )

    def mark_failed(
        self,
        operation_id: str,
        *,
        error_code: str | None,
    ) -> None:
        self._update(
            operation_id,
            status=RoutingStatus.FAILED,
            last_error_code=error_code,
        )

    def mark_outcome_unknown(
        self,
        operation_id: str,
        *,
        error_code: str | None,
    ) -> None:
        self._update(
            operation_id,
            status=RoutingStatus.OUTCOME_UNKNOWN,
            last_error_code=error_code,
        )

    def mark_reconciliation_required(
        self,
        operation_id: str,
        *,
        error_code: str | None = None,
    ) -> None:
        self._update(
            operation_id,
            status=RoutingStatus.RECONCILIATION_REQUIRED,
            last_error_code=error_code,
        )
