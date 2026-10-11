"""Approval invariants: recording decisions and authorizing routing.

These rules keep approval independent of the HTTP layer and of persistence.
They operate on a ``TriageCase`` in memory; the application service is
responsible for persisting the result atomically.
"""

from ticket_triage.domain import (
    ApprovalDecision,
    CaseStatus,
    DecisionType,
    TriageCase,
)
from ticket_triage.errors import InvalidCaseStateError
from ticket_triage.workflow import transition_case


class StaleRecommendationError(InvalidCaseStateError):
    """Raised when a decision or routing step targets an outdated recommendation."""


def record_decision(
    case: TriageCase,
    *,
    decision_id: str,
    actor_id: str,
    decision: DecisionType,
    comment: str | None = None,
) -> ApprovalDecision:
    """Record a reviewer decision and transition the case accordingly.

    Replaying the same ``decision_id`` returns the previously recorded decision
    without changing the case, which makes the operation idempotent.
    """
    existing = case.approval_decision
    if existing is not None and existing.decision_id == decision_id:
        return existing

    if case.status is not CaseStatus.PENDING_APPROVAL:
        raise InvalidCaseStateError("Case is not awaiting approval.")

    approval = ApprovalDecision(
        decision_id=decision_id,
        case_id=case.case_id,
        recommendation_version=case.recommendation_version,
        actor_id=actor_id,
        decision=decision,
        comment=comment,
    )
    new_status = (
        CaseStatus.APPROVED
        if decision is DecisionType.APPROVED
        else CaseStatus.REJECTED
    )
    transition_case(case, new_status)
    case.approval_decision = approval
    return approval


def authorize_routing(case: TriageCase, *, recommendation_version: int) -> None:
    """Confirm that an approved case may be routed.

    Raises ``StaleRecommendationError`` when the approval does not correspond to
    the recommendation version being routed, and ``InvalidCaseStateError`` when
    the case is not approved.
    """
    if case.status is not CaseStatus.APPROVED:
        raise InvalidCaseStateError("Only approved cases can be routed.")
    approval = case.approval_decision
    if approval is None:
        raise StaleRecommendationError("Case has no recorded approval.")
    if case.recommendation_version != recommendation_version:
        raise StaleRecommendationError(
            "The recommendation has changed since this decision was made."
        )
    if approval.recommendation_version != recommendation_version:
        raise StaleRecommendationError(
            "The approval was recorded for an older recommendation version."
        )
