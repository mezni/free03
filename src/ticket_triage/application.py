import logging

from ticket_triage.approval import record_decision
from ticket_triage.classification import (
    ClassificationError,
    Classifier,
)
from ticket_triage.domain import (
    CaseStatus,
    DecisionType,
    Ticket,
    TriageCase,
    validate_ticket,
)
from ticket_triage.errors import (
    ApplicationError,
    CaseNotFoundError,
    InvalidCaseStateError,
)
from ticket_triage.policy import (
    RecommendationPolicy,
    RecommendationValidationError,
)
from ticket_triage.repositories import CaseRepository
from ticket_triage.workflow import transition_case

logger = logging.getLogger("ticket_triage.application")


class TriageApplicationService:
    """Orchestrate triage use cases against a ``CaseRepository`` interface."""

    def __init__(self, repository: CaseRepository) -> None:
        self.repository = repository

    def health_check(self) -> bool:
        return self.repository.health_check()

    def create_case(
        self,
        *,
        case_id: str,
        ticket: Ticket,
        schedule_classification: bool = False,
    ) -> TriageCase:
        if not case_id.strip():
            raise ApplicationError("Case ID must not be empty.")
        errors = validate_ticket(ticket)
        if errors:
            raise ApplicationError("; ".join(errors))

        case = TriageCase(case_id=case_id, ticket=ticket)
        if schedule_classification:
            # Persist the case and its classification event in one transaction
            # so the case cannot exist without a durable record of the work.
            self.repository.create_case_with_classification_event(case)
        else:
            self.repository.create(case)
        logger.info(
            "case_created",
            extra={
                "event": "case_created",
                "case_id": case.case_id,
                "ticket_id": ticket.ticket_id,
            },
        )
        return case

    def get_case(self, case_id: str) -> TriageCase:
        case = self.repository.get(case_id)
        if case is None:
            raise CaseNotFoundError(f"Case {case_id} does not exist.")
        return case

    def start_processing(self, case_id: str) -> TriageCase:
        record = self.repository.get_with_revision(case_id)
        if record is None:
            raise CaseNotFoundError(f"Case {case_id} does not exist.")
        case = record.case
        if case.status == CaseStatus.RECEIVED:
            transition_case(case, CaseStatus.PROCESSING)
            self.repository.save_if_revision(
                case,
                expected_revision=record.revision,
            )
        return case

    def classify_case(
        self,
        case_id: str,
        *,
        classifier: Classifier,
        policy: RecommendationPolicy,
    ) -> TriageCase:
        record = self.repository.get_with_revision(case_id)
        if record is None:
            raise CaseNotFoundError(f"Case {case_id} does not exist.")
        case = record.case
        if case.status != CaseStatus.PROCESSING:
            raise InvalidCaseStateError(
                "Case must be processing before classification."
            )

        try:
            recommendation = classifier.classify(case.ticket)
            policy.validate(recommendation)
        except (
            ClassificationError,
            RecommendationValidationError,
        ) as exc:
            transition_case(case, CaseStatus.MANUAL_REVIEW)
            self.repository.save_if_revision(
                case,
                expected_revision=record.revision,
            )
            raise ApplicationError(
                "Classification failed; case sent to manual review."
            ) from exc

        case.recommendation_version += 1
        case.recommendation = recommendation
        case.approval_decision = None
        transition_case(case, CaseStatus.PENDING_APPROVAL)
        self.repository.save_if_revision(case, expected_revision=record.revision)
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

    def decide(
        self,
        case_id: str,
        *,
        decision_id: str,
        actor_id: str,
        decision: DecisionType,
        comment: str | None = None,
    ) -> TriageCase:
        record = self.repository.get_with_revision(case_id)
        if record is None:
            raise CaseNotFoundError(f"Case {case_id} does not exist.")
        case = record.case

        existing = case.approval_decision
        if existing is not None and existing.decision_id == decision_id:
            logger.info(
                "decision_replayed",
                extra={
                    "event": "decision_replayed",
                    "case_id": case.case_id,
                    "decision_id": decision_id,
                },
            )
            return case

        record_decision(
            case,
            decision_id=decision_id,
            actor_id=actor_id,
            decision=decision,
            comment=comment,
        )
        self.repository.save_if_revision(case, expected_revision=record.revision)
        logger.info(
            "decision_recorded",
            extra={
                "event": "decision_recorded",
                "case_id": case.case_id,
                "decision_id": decision_id,
                "actor_id": actor_id,
                "status": case.status.value,
            },
        )
        return case
