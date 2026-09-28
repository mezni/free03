import json
from pathlib import Path

from support_agent.models.research import (
    HistoricalTicket,
    SimilarTicket,
)


HISTORICAL_TICKET_STORE = Path(
    "data/historical_tickets.json"
)


def search_similar_tickets(
    query: str,
) -> list[dict]:

    with HISTORICAL_TICKET_STORE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    tickets = [
        HistoricalTicket.model_validate(item)
        for item in data
    ]

    query_words = set(
        query.lower().split()
    )

    results = []

    for ticket in tickets:

        text = (
            f"{ticket.subject} "
            f"{ticket.body} "
            f"{ticket.category}"
        ).lower()

        score = sum(
            1
            for word in query_words
            if word in text
        )

        if score > 0:
            results.append(
                SimilarTicket(
                    ticket_id=ticket.ticket_id,
                    subject=ticket.subject,
                    category=ticket.category,
                    resolution=ticket.resolution,
                    score=score,
                )
            )

    results.sort(
        key=lambda item: item.score,
        reverse=True,
    )

    return [
        result.model_dump()
        for result in results[:3]
    ]