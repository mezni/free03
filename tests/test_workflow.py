import pytest

from ticket_triage.domain import CaseStatus, Ticket, TriageCase
from ticket_triage.workflow import (
    InvalidTransitionError,
    transition_case,
)


def make_case() -> TriageCase:
    ticket = Ticket(
        ticket_id="T-2001",
        subject="Cannot access account",
        description="Login fails after password reset.",
    )
    return TriageCase(case_id="CASE-2001", ticket=ticket)


def test_valid_transition_updates_status():
    case = make_case()
    transition_case(case, CaseStatus.PROCESSING)
    assert case.status == CaseStatus.PROCESSING


def test_received_cannot_transition_directly_to_completed():
    case = make_case()
    with pytest.raises(InvalidTransitionError):
        transition_case(case, CaseStatus.COMPLETED)
    assert case.status == CaseStatus.RECEIVED
