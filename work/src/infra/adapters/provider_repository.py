from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.types import to_pydantic
from src.domain.provider import Provider
from src.infra.models.provider import ProviderModel
from src.interactor.dtos.provider_dtos import ProviderOutputDto
from src.interactor.interfaces.provider_repository import ProviderRepository


class SQLiteProviderRepository(ProviderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_provider(self, payload: Dict) -> Provider:
        db_item = ProviderModel(**payload)
        async with self._session() as session:
            session.add(db_item)
            await session.commit()
        return to_pydantic(db_item, ProviderOutputDto)

    async def get_provider_by_name(self, provider_name: str):
        async with self._session() as session:
            q = await session.execute(
                select(ProviderModel).where(
                    ProviderModel.provider_name == provider_name
                )
            )
            db_item = q.scalars().first()
            if db_item:
                return to_pydantic(db_item, ProviderOutputDto)
            else:
                return db_item
