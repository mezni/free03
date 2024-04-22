import pytest
from src.infra.repositories.periods_repository_in_memory import PeriodInMemoryRepository
from src.interactor.use_cases.periods_interval_load_usecase import (
    LoadPeriodIntervalUseCase,
)


def test_periods_interval_load_usecase():
    period_repo = PeriodInMemoryRepository()
    use_case = LoadPeriodIntervalUseCase(period_repo)
    period_list = ["2024-04-20", "2024-04-21"]
    result = use_case.execute(period_list)
    assert len(result) == 2
