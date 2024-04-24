from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

# from sqlalchemy.future import select
from src.database import Base
from src.interfaces import PeriodRepositoryInterface
from src.schemas import PeriodSchemaIn, PeriodSchemaOut
from src.models import PeriodModel


T = TypeVar("T", bound=BaseModel)


class SQLitePeriodRepository(PeriodRepositoryInterface):
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session()

    def to_pydantic(self, db_object: Base, pydantic_model: Type[T]) -> T:
        return pydantic_model(**db_object.__dict__)

    async def create_period(self, period_in: PeriodSchemaIn):
        async with self.async_session as session:
            item_db = PeriodModel(**period_in.model_dump())
            session.add(item_db)
            await session.commit()
            await session.refresh(item_db)
            item_out = self.to_pydantic(item_db, PeriodSchemaOut)
            return item_out
