# repositories.py
from abc import ABC, abstractmethod
from src.entities import Period


class PeriodRepositoryInterface(ABC):
    @abstractmethod
    def create_period(self, period_name: str) -> Period:
        pass
