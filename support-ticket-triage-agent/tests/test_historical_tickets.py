from support_agent.tools.historical_tickets import (
    search_similar_tickets,
)


def test_search_similar_tickets():
    results = search_similar_tickets(
        "internet router connection"
    )

    assert len(results) > 0
    assert results[0]["category"] == "technical_support"