""" Module for PeriodInMemoryRepository
"""

import uuid
from typing import List
from src.domain.entities.period import Period
from src.interactor.interfaces.repositories.period_repository import (
    PeriodRepositoryInterface,
)


from abc import ABC, abstractmethod
from typing import Optional
from src.domain.value_objects import CodeId
from src.domain.entities.period import Period


class PeriodInMemoryRepository(ABC):
    """This class is the interface for the PeriodRepository"""

    @abstractmethod
    def get_all_periods(self) -> Optional[Period]:
        """Get all Periods

        :param :
        :return: List[Period]
        """


class PeriodInMemoryRepository(PeriodRepositoryInterface):
    """InMemory Repository for Period"""

    def __init__(self) -> None:
        self._data: List[Period] = []

    def create(self, period_name: str) -> Period:
        period = Period(period_code=uuid.uuid4(), period_name=period_name)
        self._data.append(period)

        return period

    def get_by_name(self, period_name: str) -> Period:
        return None
