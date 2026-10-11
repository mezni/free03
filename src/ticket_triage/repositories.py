from dataclasses import dataclass
from typing import Protocol

from ticket_triage.domain import TriageCase


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
