import uuid
import pytest
from src.infra.repositories.period_in_memmory_repository import PeriodInMemoryRepository


def test_profession_in_memory_repository():
    repository = PeriodInMemoryRepository()
    period = repository.create(
        "2024-04-20"
    )
    
    assert len(repository._data) == 1