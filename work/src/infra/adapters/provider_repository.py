from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.provider import Provider
from src.infra.models.provider import ProviderModel
from src.interactor.interfaces.provider_repository import ProviderRepository


class SQLiteProviderRepository(ProviderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_provider(self, provider_name: str) -> Provider:
        db_item = ProviderModel(provider_name=provider_name)
        async with self._session() as session:
            session.add(db_item)
            await session.commit()
            return db_item
