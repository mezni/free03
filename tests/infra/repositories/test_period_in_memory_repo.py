from src.domain.entities.period import Period
from src.infra.repositories.period_in_memory_repo import InMemoryPeriodRepository


def test_period_in_memory_repo():
    repo = InMemoryPeriodRepository()
    result = repo.get_periods_interval()
    assert len(result) == 0
