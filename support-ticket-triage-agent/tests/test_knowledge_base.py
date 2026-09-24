from support_agent.tools.knowledge_base import (
    knowledge_base_search,
)

from support_agent.tools.registry import TOOL_FUNCTIONS

def test_knowledge_base_search():
    results = knowledge_base_search(
        "internet connection router"
    )

    assert len(results) > 0
    assert results[0]["id"] == "KB001"






def test_knowledge_base_tool_registered():
    assert "knowledge_base_search" in TOOL_FUNCTIONS


def test_create_ticket_tool_registered():
    assert "create_ticket" in TOOL_FUNCTIONS