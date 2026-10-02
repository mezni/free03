from support_agent.customer_memory import (
    add_or_update_memory,
)
from support_agent.memory_extraction import (
    extract_memory_candidates,
)
from support_agent.memory_policy import (
    should_store_memory,
)
from support_agent.models import MemoryType


def process_message_for_memory(
    message: str,
):
    extraction = extract_memory_candidates(message)

    stored_memories = []

    for candidate in extraction.memories:

        if not should_store_memory(candidate):
            continue

        memory = add_or_update_memory(
            customer_id=candidate.customer_id,
            key=candidate.key,
            value=candidate.value,
            source=candidate.source,
            memory_type=candidate.memory_type,
            confidence=candidate.confidence,
        )

        stored_memories.append(memory)

    return stored_memories