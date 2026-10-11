from ticket_triage.approval import record_decision
from ticket_triage.domain import (
    CaseStatus,
    DecisionType,
    Recommendation,
    Ticket,
    TriageCase,
)
from ticket_triage.repositories import CaseRepository
from ticket_triage.workflow import transition_case


class ApplicationError(ValueError):
    """Raised when an application use case cannot be completed."""


class TriageApplicationService:
    def __init__(self, repository: CaseRepository) -> None:
        self.repository = repository

    def create_case(
        self,
        *,
        case_id: str,
        ticket: Ticket,
    ) -> TriageCase:
        from ticket_triage.domain import validate_ticket

        if not case_id.strip():
            raise ApplicationError("Case ID must not be empty.")
        errors = validate_ticket(ticket)
        if errors:
            raise ApplicationError("; ".join(errors))
