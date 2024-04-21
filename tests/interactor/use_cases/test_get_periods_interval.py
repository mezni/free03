from src.domain.entities.period import Period
from src.infra.repositories.period_in_memory_repo import InMemoryPeriodRepository
from src.interactor.use_caces.get_periods_interval import GetPeriodsIntervalUseCase


def test_period_in_memory_repo():
    repo = InMemoryPeriodRepository()
    use_case = GetPeriodsIntervalUseCase(repo)
    result = use_case.execute()
    assert len(result) == 0
