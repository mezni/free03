"""Reconcile routing operations whose outcome is not yet confirmed.

An operation in ``OUTCOME_UNKNOWN`` or ``RECONCILIATION_REQUIRED`` must not be
resent blindly: the provider may already have committed the assignment. The
reconciler first asks the provider what it knows, using the operation's stable
idempotency key, and only then decides what to do:

============================ ===============================================
Provider lookup result       Action
============================ ===============================================
Found and success confirmed  Persist success and the external reference
Definitively absent          Retry only if the provider guarantees idempotent
                             retries; otherwise keep it unresolved
Inconclusive                 Keep unresolved and reconcile again later
Confirmed failure            Persist failure and apply the recovery policy
============================ ===============================================

The last two rows are the reason a lookup that returns no result under
eventual consistency can never be treated as proof the request never happened.
"""

import logging

from ticket_triage.domain import RoutingOperation
from ticket_triage.errors import (
    RoutingConfirmedFailure,
    RoutingLookupInconclusiveError,
    RoutingOperationNotFoundError,
)
from ticket_triage.repositories import RoutingOperationRepository
from ticket_triage.routing_provider import (
    RoutingOutcome,
    RoutingProvider,
    classify_provider_error,
)

logger = logging.getLogger("ticket_triage.reconciliation")


def _error_code(error: BaseException) -> str:
    return type(error).__name__[:64]


class RoutingReconciler:
    """Resolve unresolved routing operations against the provider's truth."""

    def __init__(
        self,
        *,
        routing_repository: RoutingOperationRepository,
        provider: RoutingProvider,
    ) -> None:
        self.routing_repository = routing_repository
        self.provider = provider

    def reconcile(self, operation_id: str) -> RoutingOperation:
        """Reconcile one operation and return its persisted state."""
        operation = self.routing_repository.get(operation_id)
        if operation is None:
            raise RoutingOperationNotFoundError(
                f"Routing operation {operation_id} does not exist."
            )

        try:
            reference = self.provider.lookup_by_idempotency_key(
                operation.idempotency_key
            )
        except RoutingLookupInconclusiveError as exc:
            return self._keep_unresolved(operation_id, exc)
        except RoutingConfirmedFailure as exc:
            self.routing_repository.mark_failed(
                operation_id,
                error_code=_error_code(exc),
            )
            return self._reload(operation_id)
        except Exception as exc:  # noqa: BLE001 - unknown lookup is not proof
            return self._keep_unresolved(operation_id, exc)

        if reference is not None:
            self.routing_repository.mark_succeeded(
                operation_id,
                external_reference=reference,
            )
            logger.info(
                "routing_reconciled_success",
                extra={
                    "event": "routing_reconciled_success",
                    "operation_id": operation_id,
                },
            )
            return self._reload(operation_id)

        # The provider definitively found no matching operation.
        if self._retry_is_safe(operation):
            return self._retry(operation)

        logger.warning(
            "routing_reconciliation_inconclusive",
            extra={
                "event": "routing_reconciliation_inconclusive",
                "operation_id": operation_id,
                "reason": "absent_without_safe_retry",
            },
        )
        self.routing_repository.mark_reconciliation_required(
            operation_id,
            error_code="absent_without_safe_retry",
        )
        return self._reload(operation_id)

    def reconcile_unresolved(self) -> list[RoutingOperation]:
        """Reconcile every operation whose outcome is not confirmed."""
        return [
            self.reconcile(operation.operation_id)
            for operation in self.routing_repository.list_unresolved()
        ]

    def _retry_is_safe(self, operation: RoutingOperation) -> bool:
        """Only retry an absent operation when the provider guarantees it.

        The capability defaults to ``False``: without an explicit provider
        guarantee, a blind retry could duplicate the side effect.
        """
        return bool(getattr(self.provider, "supports_safe_retry", False))

    def _retry(self, operation: RoutingOperation) -> RoutingOperation:
        """Resend the request using the same idempotency key."""
        operation_id = operation.operation_id
        self.routing_repository.mark_in_progress(operation_id)
        try:
            reference = self.provider.route(
                ticket_id=operation.ticket_id,
                destination=operation.destination,
                idempotency_key=operation.idempotency_key,
            )
        except BaseException as exc:  # noqa: BLE001 - classified below
            if classify_provider_error(exc) is RoutingOutcome.CONFIRMED_FAILURE:
                self.routing_repository.mark_failed(
                    operation_id,
                    error_code=_error_code(exc),
                )
            else:
                self.routing_repository.mark_outcome_unknown(
                    operation_id,
                    error_code=_error_code(exc),
                )
            return self._reload(operation_id)

        self.routing_repository.mark_succeeded(
            operation_id,
            external_reference=reference,
        )
        return self._reload(operation_id)

    def _keep_unresolved(
        self,
        operation_id: str,
        error: BaseException,
    ) -> RoutingOperation:
        logger.warning(
            "routing_reconciliation_inconclusive",
            extra={
                "event": "routing_reconciliation_inconclusive",
                "operation_id": operation_id,
                "error_code": _error_code(error),
            },
        )
        self.routing_repository.mark_reconciliation_required(
            operation_id,
            error_code=_error_code(error),
        )
        return self._reload(operation_id)

    def _reload(self, operation_id: str) -> RoutingOperation:
        operation = self.routing_repository.get(operation_id)
        if operation is None:  # pragma: no cover - defensive
            raise RoutingOperationNotFoundError(
                f"Routing operation {operation_id} vanished."
            )
        return operation


__all__ = ["RoutingReconciler"]
