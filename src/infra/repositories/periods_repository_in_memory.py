""" Module for PeriodInMemoryRepository
"""

import uuid
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
        return period
