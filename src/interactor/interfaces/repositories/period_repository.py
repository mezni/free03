""" This module contains the interface for the PeriodRepository
"""

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.value_objects import CodeId
from src.domain.entities.period import Period


class PeriodRepositoryInterface(ABC):
    """This class is the interface for the PeriodRepository"""

    @abstractmethod
    def get_by_name(self, period_name: str) -> Optional[Period]:
        """Get a Period by name

        :param period_name: period_name
        :return: Period
        """

    @abstractmethod
    def create(self, period_name: str) -> Optional[Period]:
        """Create a Period

        :param period_name: period name
        :return: Period
        """
