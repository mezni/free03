from datetime import datetime, timezone

from support_agent.memory_repository import MemoryRepository
from support_agent.models import (
    CustomerMemory,
    MemorySource,
    MemoryType,
)


def seed_memory_evaluation_data():

    repository = MemoryRepository()

    now = datetime.now(timezone.utc)

    memories = [
        CustomerMemory(
            memory_id="E001",
            customer_id="C001",
            key="preferred_contact_method",
            value="email",
            memory_type=MemoryType.PREFERENCE,
            source=MemorySource.CUSTOMER_STATEMENT,
            confidence=0.95,
            created_at=now,
            updated_at=now,
        ),
        CustomerMemory(
            memory_id="E002",
            customer_id="C001",
            key="product",
            value="mobile application",
            memory_type=MemoryType.PRODUCT,
            source=MemorySource.CUSTOMER_STATEMENT,
            confidence=0.95,
            created_at=now,
            updated_at=now,
        ),
        CustomerMemory(
            memory_id="E003",
            customer_id="C002",
            key="preferred_contact_method",
            value="phone",
            memory_type=MemoryType.PREFERENCE,
            source=MemorySource.CUSTOMER_STATEMENT,
            confidence=0.95,
            created_at=now,
            updated_at=now,
        ),
    ]

    for memory in memories:
        repository.save(memory)