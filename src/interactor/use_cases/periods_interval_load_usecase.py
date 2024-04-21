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
        period = Period(uuid.uuid4(), period_list[0])
        self.period_repo.create_period(period)
        return []
