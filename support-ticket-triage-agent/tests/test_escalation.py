import json

from support_agent.tools.escalation import (
    escalate_to_human,
)


def test_escalate_to_human(tmp_path, monkeypatch):
    store = tmp_path / "escalations.json"

    monkeypatch.setattr(
        "support_agent.tools.escalation.ESCALATION_STORE",
        store,
    )

    result = escalate_to_human(
        ticket_id="T005",
        reason="Possible account compromise.",
        priority="critical",
    )

    assert result["escalation_id"] == "E001"
    assert result["ticket_id"] == "T005"
    assert result["status"] == "escalated"

    with store.open(
        "r",
        encoding="utf-8",
    ) as file:
        escalations = json.load(file)

    assert len(escalations) == 1
    assert escalations[0]["ticket_id"] == "T005"
    assert escalations[0]["priority"] == "critical"