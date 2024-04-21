""" This module contains the interface for the PeriodRepository
"""

from abc import ABC, abstractmethod
from typing import Optional, List

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

    @abstractmethod
    def create_periods_interval(
        self, period_name_min: str, period_name_max: str
    ) -> List[Period]:
        """Create Periods interval

        :param period_name_min: period_name_min
        :param period_name_max: period_name_max
        :return: Period List
        """

    @abstractmethod
    def get_period_by_name(self, period_name: str) -> Optional[Period]:
        """Get Period by name

        :param name : period_name
        :param description : period name
        :return: Period
        """
