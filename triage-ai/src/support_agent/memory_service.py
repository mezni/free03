from support_agent.customer_memory import (
    add_or_update_memory,
    delete_memory,
    get_customer_memories,
)
from support_agent.memory_expiration import (
    remove_expired_memories,
)
from support_agent.memory_extraction import (
    extract_memory_candidates,
)
from support_agent.memory_policy import (
    should_store_memory,
)
from support_agent.memory_retrieval import (
    retrieve_relevant_memories,
    format_retrieved_memories,
)
from support_agent.models import (
    CustomerMemory,
    MemoryCandidate,
    RetrievedMemory,
)


class MemoryService:

    def process_message(
        self,
        message: str,
    ) -> list[CustomerMemory]:
        """
        Extract and persist valid long-term memories
        from a customer message.
        """

        extraction = extract_memory_candidates(message)

        stored_memories = []

        for candidate in extraction.memories:
            if not should_store_memory(candidate):
                continue

            memory = add_or_update_memory(
                customer_id=candidate.customer_id,
                key=candidate.key,
                value=candidate.value,
                memory_type=candidate.memory_type,
                source=candidate.source,
                confidence=candidate.confidence,
            )

            if memory is not None:
                stored_memories.append(memory)

        return stored_memories

    def retrieve(
        self,
        customer_id: str,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedMemory]:
        """
        Retrieve memories relevant to the current request.
        """

        return retrieve_relevant_memories(
            customer_id=customer_id,
            query=query,
            limit=limit,
        )

    def get_context(
        self,
        customer_id: str,
        query: str,
        limit: int = 5,
    ) -> str:
        memories = self.retrieve(
            customer_id=customer_id,
            query=query,
            limit=limit,
        )

        return format_retrieved_memories(memories)

    def get_customer_memories(
        self,
        customer_id: str,
    ) -> list[CustomerMemory]:
        """
        Return all non-expired memories for a customer.
        """

        return get_customer_memories(customer_id)

    def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a specific memory.
        """

        return delete_memory(memory_id)

    def remove_expired(self) -> int:
        """
        Permanently remove expired memories.
        """

        return remove_expired_memories()