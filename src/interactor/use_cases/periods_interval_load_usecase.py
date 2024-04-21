""" This module is responsible for load Period interval.
"""

from typing import List
from src.domain.entities.period import Period


class LoadPeriodIntervalUseCase:
    """This class is responsible for load Period interval."""

    def __init__(self):
        pass

    def execute(self, period_list: List[str]) -> List[Period]:
        return []
