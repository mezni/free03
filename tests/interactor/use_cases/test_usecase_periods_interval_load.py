import pytest
from src.interactor.use_cases.usecase_periods_interval_load import (
    DumpPeriodIntervalCase,
)


def test_usecase_periods_interval_load():
    use_case = DumpPeriodIntervalCase()
    period_list = []
    result = use_case.execute(period_list)
