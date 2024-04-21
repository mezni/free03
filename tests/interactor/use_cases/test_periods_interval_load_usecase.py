import pytest
from src.infra.repositories.periods_repository_in_memory import PeriodInMemoryRepository


def test_periods_interval_load_usecase():
    period_repo = PeriodInMemoryRepository()


#    use_case = LoadPeriodIntervalUseCase()
#    period_list = []
#    result = use_case.execute(period_list)
