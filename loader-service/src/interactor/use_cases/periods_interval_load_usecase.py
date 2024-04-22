""" This module is responsible for load Period interval.
"""

import uuid
from typing import List
from src.domain.entities.period import Period
from src.interactor.interfaces.periods_repository_interface import (
    PeriodRepositoryInterface,
)


class LoadPeriodIntervalUseCase:
    """This class is responsible for load Period interval."""

    def __init__(self, period_repo: PeriodRepositoryInterface):
        self.period_repo = period_repo

    def execute(self, period_list: List[str]) -> List[Period]:
        result = self.period_repo.create_periods_interval(
            min(period_list), max(period_list)
        )
        return result
