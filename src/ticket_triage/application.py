import logging

from ticket_triage.classification import (
    ClassificationError,
    Classifier,
)
from ticket_triage.domain import (
    CaseStatus,
    Ticket,
    TriageCase,
)
from ticket_triage.policy import (
    RecommendationPolicy,
    RecommendationValidationError,
)
from ticket_triage.repositories import CaseRepository
from ticket_triage.workflow import transition_case

logger = logging.getLogger("ticket_triage.application")


class ApplicationError(ValueError):
    """Raised when an application use case cannot be completed."""


class TriageApplicationService:
    def __init__(self, repository: CaseRepository) -> None:
        self.repository = repository

    def health_check(self) -> bool:
        return self.repository.health_check()

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

    def classify_case(
        self,
        case_id: str,
        *,
        classifier: Classifier,
        policy: RecommendationPolicy,
    ) -> TriageCase:
        case = self.get_case(case_id)
        if case.status != CaseStatus.PROCESSING:
            raise ApplicationError("Case must be processing before classification.")
        try:
            recommendation = classifier.classify(case.ticket)
            policy.validate(recommendation)
        except (
            ClassificationError,
            RecommendationValidationError,
        ) as exc:
            transition_case(case, CaseStatus.MANUAL_REVIEW)
            self.repository.save(case)
            raise ApplicationError(
                "Classification failed; case sent to manual review."
            ) from exc
        case.recommendation_version += 1
        case.recommendation = recommendation
        case.approval_decision = None
        transition_case(case, CaseStatus.PENDING_APPROVAL)
        self.repository.save(case)
        logger.info(
            "classification_completed",
            extra={
                "event": "classification_completed",
                "case_id": case.case_id,
                "ticket_id": case.ticket.ticket_id,
                "recommendation_version": case.recommendation_version,
                "status": case.status.value,
            },
        )
        return case
