"""Security invariants for the workflow transition table.

These assertions read ``ALLOWED_TRANSITIONS`` directly, so they execute even
though ``transition_case()`` and ``InvalidTransitionError`` are not yet
implemented. They encode the rule that an untrusted classification output can
never bypass human approval before routing.
"""

from ticket_triage.domain import CaseStatus
from ticket_triage.workflow import ALLOWED_TRANSITIONS


def test_rejected_cases_cannot_be_routed():
    assert CaseStatus.ROUTING not in ALLOWED_TRANSITIONS[CaseStatus.REJECTED]


def test_model_output_cannot_transition_directly_to_approved():
    # Classification states must pass through PENDING_APPROVAL; neither
    # RECEIVED nor PROCESSING may jump straight to APPROVED.
    assert CaseStatus.APPROVED not in ALLOWED_TRANSITIONS[CaseStatus.RECEIVED]
    assert CaseStatus.APPROVED not in ALLOWED_TRANSITIONS[CaseStatus.PROCESSING]


def test_pending_approval_cannot_skip_to_routing():
    assert CaseStatus.ROUTING not in ALLOWED_TRANSITIONS[CaseStatus.PENDING_APPROVAL]


def test_only_approved_cases_can_be_routed():
    routing_sources = {
        status
        for status, targets in ALLOWED_TRANSITIONS.items()
        if CaseStatus.ROUTING in targets
    }
    assert routing_sources == {CaseStatus.APPROVED}
