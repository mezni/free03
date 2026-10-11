from dataclasses import dataclass
from typing import Protocol

from ticket_triage.domain import RoutingOperation, TriageCase


@dataclass(frozen=True)
class CaseRecord:
    """A persisted case together with the revision it was read at.

    The revision is the value a caller must present back to
    ``save_if_revision`` to perform a compare-and-swap update.
    """

    case: TriageCase
    revision: int


class CaseRepository(Protocol):
    """Contract for storing and retrieving triage cases."""

    def create(self, case: TriageCase) -> None:
        """Insert a new case, failing if the case ID already exists."""
        ...

    def create_case_with_classification_event(self, case: TriageCase) -> None:
        """Insert a case and its classification outbox event atomically.

        Both records commit together or neither does, so a case can never be
        persisted without a durable record of the classification work it
        requires. Fails if the case ID already exists.
        """
        ...

    def save(self, case: TriageCase) -> None:
        """Persist a triage case, inserting or overwriting it."""
        ...

    def get(self, case_id: str) -> TriageCase | None:
        """Return a case, or None if it does not exist."""
        ...

    def get_with_revision(self, case_id: str) -> CaseRecord | None:
        """Return a case and its current revision, or None if absent."""
        ...

    def save_if_revision(self, case: TriageCase, expected_revision: int) -> None:
        """Persist a case only if it is still at ``expected_revision``.

        Raises ``ConcurrentUpdateError`` when another writer has advanced the
        revision since it was read.
        """
        ...

    def health_check(self) -> bool:
        """Return whether the repository can serve basic operations."""
        ...


class RoutingOperationRepository(Protocol):
    """Contract for durably storing routing operations."""

    def create_or_get(
        self,
        operation: RoutingOperation,
    ) -> tuple[RoutingOperation, bool]:
        """Insert ``operation`` or return the existing one for its key.

        Returns ``(operation, created)`` where ``created`` is False when an
        operation with the same idempotency key already existed.
        """
        ...

    def get(self, operation_id: str) -> RoutingOperation | None:
        """Return an operation, or None if it does not exist."""
        ...

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> RoutingOperation | None:
        """Return the operation for a key, or None if it does not exist."""
        ...

    def list_unresolved(self) -> list[RoutingOperation]:
        """Return operations whose outcome is not yet confirmed."""
        ...

    def mark_in_progress(self, operation_id: str) -> None:
        """Record that a provider request is being attempted."""
        ...

    def mark_succeeded(
        self,
        operation_id: str,
        *,
        external_reference: str,
    ) -> None:
        """Record a provider-confirmed success and its reference."""
        ...

    def mark_failed(
        self,
        operation_id: str,
        *,
        error_code: str | None,
    ) -> None:
        """Record a provider-confirmed failure."""
        ...

    def mark_outcome_unknown(
        self,
        operation_id: str,
        *,
        error_code: str | None,
    ) -> None:
        """Record that the outcome is unknown and must be reconciled."""
        ...

    def mark_reconciliation_required(
        self,
        operation_id: str,
        *,
        error_code: str | None = None,
    ) -> None:
        """Record that reconciliation could not yet resolve the outcome."""
        ...
