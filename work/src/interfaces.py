from typing import Optional
from abc import ABC, abstractmethod
from src.schemas import PeriodSchemaIn, PeriodSchemaOut


class PeriodRepositoryInterface(ABC):
    @abstractmethod
    async def create_period(
        self, period_in: PeriodSchemaIn
    ) -> Optional[PeriodSchemaOut]:
        pass

    @abstractmethod
    async def get_period_by_name(
        self, period_in: PeriodSchemaIn
    ) -> Optional[PeriodSchemaOut]:
        pass
