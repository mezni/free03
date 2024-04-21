""" Module for PeriodInMemoryRepository
"""

import uuid
from datetime import datetime, timedelta
from typing import List
from src.domain.entities.period import Period
from src.interactor.interfaces.periods_repository_interface import (
    PeriodRepositoryInterface,
)


class PeriodInMemoryRepository(PeriodRepositoryInterface):
    """InMemory Repository for Period"""

    def __init__(self) -> None:
        self._periods: List[Period] = []

    def create_period(self, period_name: str) -> Period:
        period = Period(period_code=uuid.uuid4(), period_name=period_name)
        self._periods.append(period)
        return period

    def create_periods_interval(
        self, period_name_min: str, period_name_max: str
    ) -> List[Period]:
        result = []
        period_name_date_curr = datetime.strptime(period_name_min, "%Y-%m-%d")
        while period_name_date_curr <= datetime.strptime(period_name_max, "%Y-%m-%d"):
            period_name_curr = period_name_date_curr.strftime("%Y-%m-%d")
            stored_period = self.get_period_by_name(period_name_curr)
            if not stored_period:
                stored_period = self.create_period(period_name_curr)
            result.append(stored_period)
            period_name_date_curr += timedelta(days=1)
        return result

    def get_period_by_name(self, period_name: str) -> Period:
        result = next((p for p in self._periods if p.period_name == period_name), None)
        return result
