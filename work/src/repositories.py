from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.models import PeriodModel
from src.dtos import CreatePeriodDTO, PeriodDTO


class SQLitePeriodRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session()

    async def create_period(self, period_dto: CreatePeriodDTO):
        async with self.async_session as session:
            new_period_dto = PeriodDTO(**period_dto.to_dict())
            new_period_item = PeriodModel(**new_period_dto.to_dict())
            session.add(new_period_item)
            await session.commit()
