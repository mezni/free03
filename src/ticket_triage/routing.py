"""Durable routing orchestration.

The safe execution sequence is:

1. Verify the case has a valid, current approval.
2. Create or retrieve the routing operation using its stable idempotency key.
3. Commit the routing intent to the database.
4. Mark the operation as in progress and commit that state.
5. Call the external provider outside the database transaction.
6. Persist confirmed success, confirmed failure, or unknown outcome.
7. Mark the case completed only after confirmed success.

The routing operation and the case have separate lifecycles. A case reaches
``COMPLETED`` only when there is persisted evidence of confirmed success; a
timeout leaves the case in ``ROUTING`` and the operation unresolved.
"""

import logging
import uuid

from ticket_triage.approval import authorize_routing
from ticket_triage.domain import (
    CaseStatus,
    RoutingOperation,
    RoutingStatus,
)
from ticket_triage.errors import (
    CaseNotFoundError,
    RoutingOperationNotFoundError,
)
from ticket_triage.idempotency import routing_idempotency_key
from ticket_triage.repositories import (
    CaseRepository,
    RoutingOperationRepository,
)
from ticket_triage.routing_provider import (
    RoutingOutcome,
    RoutingProvider,
    classify_provider_error,
)
from ticket_triage.workflow import transition_case

logger = logging.getLogger("ticket_triage.routing")


def _error_code(error: BaseException) -> str:
    """Return a safe, bounded error classification.

    Only the exception type is recorded. Raw messages may contain credentials,
    ticket content, or provider response bodies and must never be persisted.
    """
    return type(error).__name__[:64]


class RoutingService:
    """Orchestrate routing use cases across case, operation, and provider."""

    def __init__(
        self,
        *,
        case_repository: CaseRepository,
        routing_repository: RoutingOperationRepository,
        provider: RoutingProvider,
    ) -> None:
        self.case_repository = case_repository
        self.routing_repository = routing_repository
        self.provider = provider

    def request_routing(
        self,
        case_id: str,
        *,
        operation_id: str | None = None,
    ) -> RoutingOperation:
        """Persist the intent to route an approved case.

        The intent is committed before any external call. Repeating the request
        for the same case and recommendation version returns the existing
        operation instead of creating a second one.
        """
        record = self.case_repository.get_with_revision(case_id)
        if record is None:
            raise CaseNotFoundError(f"Case {case_id} does not exist.")
        case = record.case

        key = routing_idempotency_key(case_id, case.recommendation_version)
        existing = self.routing_repository.get_by_idempotency_key(key)
        if existing is not None:
            return existing

        authorize_routing(case, recommendation_version=case.recommendation_version)

        approval = case.approval_decision
        if approval is None or case.recommendation is None:  # pragma: no cover
            raise CaseNotFoundError(f"Case {case_id} is not ready to route.")

        operation = RoutingOperation(
            operation_id=operation_id or uuid.uuid4().hex,
            case_id=case_id,
            approval_decision_id=approval.decision_id,
            recommendation_version=case.recommendation_version,
            idempotency_key=key,
            ticket_id=case.ticket.ticket_id,
            destination=case.recommendation.destination,
        )
        stored, created = self.routing_repository.create_or_get(operation)

        if created:
            transition_case(case, CaseStatus.ROUTING)
            self.case_repository.save_if_revision(
                case,
                expected_revision=record.revision,
            )
            logger.info(
                "routing_intent_persisted",
                extra={
                    "event": "routing_intent_persisted",
                    "case_id": case_id,
                    "operation_id": stored.operation_id,
                    "idempotency_key": stored.idempotency_key,
                },
            )
        return stored

    def execute(self, operation_id: str) -> RoutingOperation:
        """Attempt the external call and persist whatever is known.

        The provider call happens outside any database transaction. Confirmed
        success completes the case; confirmed failure is recorded; anything else
        remains an unknown outcome to be reconciled.
        """
        operation = self.routing_repository.get(operation_id)
        if operation is None:
            raise RoutingOperationNotFoundError(
                f"Routing operation {operation_id} does not exist."
            )

        if operation.status is RoutingStatus.SUCCEEDED:
            self._complete_case(operation)
            return operation

        self.routing_repository.mark_in_progress(operation_id)

        try:
            external_reference = self.provider.route(
                ticket_id=operation.ticket_id,
                destination=operation.destination,
                idempotency_key=operation.idempotency_key,
            )
        except BaseException as exc:  # noqa: BLE001 - classified below
            self._persist_failure_or_unknown(operation_id, exc)
        else:
            self.routing_repository.mark_succeeded(
                operation_id,
                external_reference=external_reference,
            )
            self._complete_case(operation)

        result = self.routing_repository.get(operation_id)
        if result is None:  # pragma: no cover - defensive
            raise RoutingOperationNotFoundError(
                f"Routing operation {operation_id} vanished."
            )
        return result

    def reconcile_operation(self, operation_id: str) -> RoutingOperation:
        """Reconcile one unresolved operation and complete the case on success.

        This imports the reconciler lazily to keep the operation-level decision
        logic in ``reconciliation.py`` and avoid an import cycle.
        """
        from ticket_triage.reconciliation import RoutingReconciler

        reconciler = RoutingReconciler(
            routing_repository=self.routing_repository,
            provider=self.provider,
        )
        result = reconciler.reconcile(operation_id)
        if result.status is RoutingStatus.SUCCEEDED:
            self._complete_case(result)
        return result

    def _persist_failure_or_unknown(
        self,
        operation_id: str,
        error: BaseException,
    ) -> None:
        code = _error_code(error)
        outcome = classify_provider_error(error)
        if outcome is RoutingOutcome.CONFIRMED_FAILURE:
            self.routing_repository.mark_failed(operation_id, error_code=code)
            logger.warning(
                "routing_confirmed_failure",
                extra={
                    "event": "routing_confirmed_failure",
                    "operation_id": operation_id,
                    "error_code": code,
                },
            )
        else:
            self.routing_repository.mark_outcome_unknown(
                operation_id,
                error_code=code,
            )
            logger.warning(
                "routing_outcome_unknown",
                extra={
                    "event": "routing_outcome_unknown",
                    "operation_id": operation_id,
                    "error_code": code,
                },
            )

    def _complete_case(self, operation: RoutingOperation) -> None:
        """Move the case to completed only after confirmed routing success."""
        record = self.case_repository.get_with_revision(operation.case_id)
        if record is None:
            raise CaseNotFoundError(f"Case {operation.case_id} does not exist.")
        case = record.case
        if case.status is CaseStatus.ROUTING:
            transition_case(case, CaseStatus.COMPLETED)
            self.case_repository.save_if_revision(
                case,
                expected_revision=record.revision,
            )
            logger.info(
                "case_completed",
                extra={
                    "event": "case_completed",
                    "case_id": case.case_id,
                    "operation_id": operation.operation_id,
                },
            )


__all__ = ["RoutingService"]
