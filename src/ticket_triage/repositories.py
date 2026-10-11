from typing import Protocol

from ticket_triage.domain import TriageCase


class CaseRepository(Protocol):
    """Contract for storing and retrieving triage cases."""

    def save(self, case: TriageCase) -> None:
        """Persist a triage case."""
        ...

    def get(self, case_id: str) -> TriageCase | None:
        """Return a case, or None if it does not exist."""
        ...
