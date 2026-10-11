from ticket_triage.domain import (
    CaseStatus,
    Priority,
    Recommendation,
    Ticket,
    TriageCase,
    validate_ticket,
)


def test_valid_ticket_has_no_validation_errors():
    ticket = Ticket(
        ticket_id="T-1001",
        subject="Cannot log in",
        description="The password reset link does not work.",
    )

    assert validate_ticket(ticket) == []
