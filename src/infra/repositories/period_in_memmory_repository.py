""" Module for PeriodInMemoryRepository
"""

import uuid
from typing import List, Optional
from src.domain.entities.period import Period

# from src.interactor.interfaces.repositories.period_repository import (
#    PeriodRepositoryInterface,
# )


class PeriodInMemoryRepository:
    """InMemory Repository for Period"""

    def __init__(self) -> None:
        self._periods: List[Period] = []

    def get_all_periods(self) -> Optional[Period]:
        """Get all Periods

        :param :
        :return: List[Period]
        """
        return self._periods
