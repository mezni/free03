import pytest

from support_agent.models.tool_result import (
    ToolExecutionResult,
)
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.registry import TOOL_FUNCTIONS


def test_dispatch_knowledge_base_search():
    result = dispatch_tool(
        "knowledge_base_search",
        {
            "query": "internet connection router"
        },
    )

    assert result.success is True
    assert len(result.data) > 0
    assert result.data[0]["id"] == "KB001"


def test_unknown_tool_raises_error():
    result = dispatch_tool(
        "does_not_exist",
        {},
    )

    assert result.success is False
    assert result.error == f"Unknown tool: does_not_exist"
    assert result.error_type == "UnknownTool"


def test_tool_failure_is_returned_as_result(
    monkeypatch,
):
    def broken_tool(query: str):
        raise RuntimeError("Service unavailable")

    monkeypatch.setitem(
        TOOL_FUNCTIONS,
        "broken_tool",
        broken_tool,
    )

    result = dispatch_tool(
        "broken_tool",
        {
            "query": "test",
        },
    )

    assert result.success is False
    assert result.error == "Service unavailable"
    assert result.error_type == "RuntimeError"


def test_dispatch_create_ticket(tmp_path, monkeypatch):
    store = tmp_path / "created_tickets.json"

    monkeypatch.setattr(
        "support_agent.tools.ticketing.TICKET_STORE",
        store,
    )

    result = dispatch_tool(
        "create_ticket",
        {
            "customer_id": "C100",
            "subject": "Billing issue",
            "description": "Customer needs billing investigation.",
            "priority": "medium",
        },
    )

    assert result.success is True
    assert result.data["status"] == "created"
    assert result.data["ticket_id"] == "CT001"


def test_dispatch_escalate_to_human(
    tmp_path,
    monkeypatch,
):
    store = tmp_path / "escalations.json"

    monkeypatch.setattr(
        "support_agent.tools.escalation.ESCALATION_STORE",
        store,
    )

    result = dispatch_tool(
        "escalate_to_human",
        {
            "ticket_id": "T005",
            "reason": "Possible account compromise.",
            "priority": "critical",
        },
    )

    assert result.success is True
    assert result.data["status"] == "escalated"
    assert result.data["ticket_id"] == "T005"