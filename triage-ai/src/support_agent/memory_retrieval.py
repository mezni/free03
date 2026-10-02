from support_agent.customer_memory import (
    get_customer_memories,
)
from support_agent.models import RetrievedMemory


def retrieve_relevant_memories(
    customer_id: str,
    query: str,
    limit: int = 5,
) -> list[RetrievedMemory]:

    memories = get_customer_memories(customer_id)

    query_words = {
        word.strip(".,!?;:").lower()
        for word in query.split()
    }

    results: list[RetrievedMemory] = []

    for memory in memories:

        searchable_text = (
            f"{memory.key} "
            f"{memory.value}"
        ).lower()

        score = sum(
            1
            for word in query_words
            if word in searchable_text
        )

        if score > 0:
            results.append(
                RetrievedMemory(
                    memory=memory,
                    relevance_score=score,
                )
            )

    results.sort(
        key=lambda item: item.relevance_score,
        reverse=True,
    )

    return results[:limit]


def format_retrieved_memories(
    memories: list[RetrievedMemory],
) -> str:

    if not memories:
        return "No relevant customer memories found."

    lines = []

    for item in memories:
        memory = item.memory

        lines.append(
            f"- {memory.key}: {memory.value}"
        )

    return "\n".join(lines)