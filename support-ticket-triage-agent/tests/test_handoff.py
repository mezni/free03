from support_agent.models.handoff import (
    ResearchRequest,
)


def test_research_request_contains_context():

    request = ResearchRequest(
        ticket_id="T001",
        customer_id="C001",
        issue_summary="Internet connection is down",
        category="technical_support",
        urgency="high",
        product="internet",
        priority="high",
        research_question=(
            "Find similar internet outage cases."
        ),
    )

    assert request.ticket_id == "T001"
    assert request.customer_id == "C001"
    assert request.category == "technical_support"
    assert request.urgency == "high"
    assert request.product == "internet"
    assert request.priority == "high"


def test_research_agent_has_only_research_tools():

    from support_agent.tools.agent_tools import (
        RESEARCH_AGENT_TOOLS,
    )

    names = {
        tool["name"]
        for tool in RESEARCH_AGENT_TOOLS
    }

    assert names == {
        "search_similar_tickets"
    }


def test_support_agent_has_only_support_tools():

    from support_agent.tools.agent_tools import (
        SUPPORT_AGENT_TOOLS,
    )

    names = {
        tool["name"]
        for tool in SUPPORT_AGENT_TOOLS
    }

    assert names == {
        "knowledge_base_search",
        "create_ticket",
        "escalate_to_human",
    }