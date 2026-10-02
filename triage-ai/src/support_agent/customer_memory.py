from datetime import datetime, timezone

from support_agent.memory_repository import MemoryRepository
from support_agent.models import (
    CustomerMemory,
    MemoryDecision,
    MemorySource,
    MemoryType,
)
from support_agent.memory_expiration import calculate_expiration
from support_agent.memory_conflict import resolve_memory_conflict

# Backward-compatible module-level list
MEMORIES: list = []

def _generate_memory_id() -> str:
    import uuid
    return f"M-{uuid.uuid4().hex[:8].upper()}"


def _init_memories():
    """Initialize MEMORIES list from repository if available."""
    global MEMORIES
    # MEMORIES is kept for backward compatibility;
    # in normal operation, the repository is the source of truth.
    # For now, MEMORIES starts empty and gets populated
    # as memories are added through the repository.
    global MEMORIES
    MEMORIES = []


def add_or_update_memory(
    *,
    customer_id: str,
    key: str,
    value: str,
    memory_type: MemoryType,
    source: MemorySource,
    confidence: float,
    repository: MemoryRepository | None = None,
) -> CustomerMemory | None:

    if repository is None:
        # Backward compatibility: use MEMORIES list
        repository = MemoryRepository()

    existing_memories = repository.get_by_customer(customer_id)

    existing = next(
        (
            memory
            for memory in existing_memories
            if memory.key == key
        ),
        None,
    )

    now = datetime.now(timezone.utc)

    if existing is None:
        memory = CustomerMemory(
            memory_id=_generate_memory_id(),
            customer_id=customer_id,
            key=key,
            value=value,
            memory_type=memory_type,
            source=source,
            confidence=confidence,
            created_at=now,
            updated_at=now,
            expires_at=calculate_expiration(memory_type),
        )

        repository.save(memory)

        # Also add to MEMORIES list for backward compatibility
        if memory not in MEMORIES:
            MEMORIES.append(memory)

        return memory

    decision = resolve_memory_conflict(
        existing=existing,
        candidate_source=source,
        candidate_confidence=confidence,
    )

    if decision == MemoryDecision.KEEP_EXISTING:
        return existing

    existing.value = value
    existing.memory_type = memory_type
    existing.source = source
    existing.confidence = confidence
    existing.updated_at = now
    existing.expires_at = calculate_expiration(memory_type)

    repository.save(existing)

    # Update in MEMORIES list
    if existing in MEMORIES:
        idx = MEMORIES.index(existing)
        MEMORIES[idx] = existing

    return existing


def get_customer_memories(
    customer_id: str,
    repository: MemoryRepository | None = None,
) -> list[CustomerMemory]:

    if repository is None:
        repository = MemoryRepository()

    return repository.get_by_customer(customer_id)


def delete_memory(
    memory_id: str,
    repository: MemoryRepository | None = None,
) -> bool:

    if repository is None:
        repository = MemoryRepository()

    return repository.delete(memory_id)