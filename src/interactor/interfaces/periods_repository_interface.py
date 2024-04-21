""" This module contains the interface for the PeriodRepository
"""

from abc import ABC, abstractmethod
from typing import Optional

""" This module contains the interface for the PeriodRepository
"""
from src.domain.value_objects import CodeId
from src.domain.entities.period import Period


class PeriodRepositoryInterface(ABC):
    """This class is the interface for the PeriodRepository"""

    @abstractmethod
    def create_period(self, period_name: str) -> Optional[Period]:
        """Create Period

        :param name : period_name
        :param description : period name
        :return: Period
        """
