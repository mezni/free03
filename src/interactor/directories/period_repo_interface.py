""" This module contains the interface for the PeriodRepository
"""

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.value_objects import CodeId
from src.domain.entities.period import Period


class PeriodRepositoryInterface(ABC):
    """This class is the interface for the PeriodRepository"""

    @abstractmethod
    def get_periods_interval(self) -> Optional[Period]:
        """Get a Period interval

        :param :
        :return: List of Period
        """
