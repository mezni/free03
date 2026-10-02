from support_agent.models import MemoryType


ALWAYS_RELEVANT_MEMORY_TYPES = {
    MemoryType.PREFERENCE,
    MemoryType.PROFILE,
}

CONTEXTUAL_MEMORY_TYPES = {
    MemoryType.ACCOUNT,
    MemoryType.PRODUCT,
}


def is_always_relevant(memory_type: MemoryType) -> bool:
    return memory_type in ALWAYS_RELEVANT_MEMORY_TYPES