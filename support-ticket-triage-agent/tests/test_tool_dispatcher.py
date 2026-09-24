import pytest

from support_agent.tools.dispatcher import dispatch_tool


def test_dispatch_knowledge_base_search():
    results = dispatch_tool(
        "knowledge_base_search",
        {
            "query": "internet connection router"
        },
    )

    assert len(results) > 0
    assert results[0]["id"] == "KB001"


def test_unknown_tool_raises_error():
    with pytest.raises(ValueError, match="Unknown tool"):
        dispatch_tool(
            "does_not_exist",
            {},
        )