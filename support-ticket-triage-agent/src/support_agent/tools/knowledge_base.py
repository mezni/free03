import json
from pathlib import Path


def knowledge_base_search(query: str) -> list[dict]:
    file_path = Path("data/knowledge_base.json")

    with file_path.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    query_words = set(query.lower().split())

    results = []

    for article in articles:
        text = (
            article["title"] + " " + article["content"]
        ).lower()

        score = sum(
            1 for word in query_words
            if word in text
        )

        if score > 0:
            results.append(
                {
                    "id": article["id"],
                    "title": article["title"],
                    "content": article["content"],
                    "score": score,
                }
            )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:3]