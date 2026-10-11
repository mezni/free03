"""Domain rules for controlling ticket-triage workflow state transitions.

Why centralize transitions?
The transition table becomes the single source of truth for legal workflow
changes. Later, an API endpoint or background worker can call
``transition_case()`` rather than implementing its own rules.

Notice that APPROVED can move to ROUTING, but PENDING_APPROVAL cannot. This
prevents the workflow from skipping the approval state.

Important limitation: this is an in-memory domain rule. In production, the
backend must also enforce authorization and persist state changes safely,
including protection against concurrent requests.
"""

from ticket_triage.domain import CaseStatus, TriageCase

ALLOWED_TRANSITIONS: dict[CaseStatus, set[CaseStatus]] = {
    CaseStatus.RECEIVED: {
        CaseStatus.PROCESSING,
        CaseStatus.MANUAL_REVIEW,
    },
    CaseStatus.PROCESSING: {
        CaseStatus.PENDING_APPROVAL,
        CaseStatus.MANUAL_REVIEW,
    },
    CaseStatus.PENDING_APPROVAL: {
        CaseStatus.APPROVED,
        CaseStatus.REJECTED,
        CaseStatus.MANUAL_REVIEW,
    },
    CaseStatus.APPROVED: {
        CaseStatus.ROUTING,
        CaseStatus.MANUAL_REVIEW,
    },
    CaseStatus.REJECTED: set(),
    CaseStatus.ROUTING: {
        CaseStatus.COMPLETED,
        CaseStatus.MANUAL_REVIEW,
    },
    CaseStatus.COMPLETED: set(),
    CaseStatus.MANUAL_REVIEW: set(),
}


class InvalidTransitionError(ValueError):
    """Raised when a case attempts an illegal state transition."""
