import uuid
import pytest
from src.infra.repositories.period_in_memmory_repository import PeriodInMemoryRepository


def test_profession_in_memory_repository():
    repository = PeriodInMemoryRepository()

    assert len(repository._periods) == 0
