import json
from pathlib import Path

from support_agent.models.escalation import (
    EscalateToHumanInput,
    EscalateToHumanResult,
)


ESCALATION_STORE = Path("data/escalations.json")


def escalate_to_human(
    ticket_id: str,
    reason: str,
    priority: str,
) -> dict:

    input_data = EscalateToHumanInput(
        ticket_id=ticket_id,
        reason=reason,
        priority=priority,
    )

    ESCALATION_STORE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if ESCALATION_STORE.exists():
        with ESCALATION_STORE.open(
            "r",
            encoding="utf-8",
        ) as file:
            escalations = json.load(file)
    else:
        escalations = []

    escalation_id = f"E{len(escalations) + 1:03d}"

    escalation = {
        "escalation_id": escalation_id,
        "ticket_id": input_data.ticket_id,
        "reason": input_data.reason,
        "priority": input_data.priority,
        "status": "escalated",
    }

    escalations.append(escalation)

    with ESCALATION_STORE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            escalations,
            file,
            indent=2,
        )

    result = EscalateToHumanResult(
        escalation_id=escalation_id,
        ticket_id=input_data.ticket_id,
        status="escalated",
    )

    return result.model_dump()