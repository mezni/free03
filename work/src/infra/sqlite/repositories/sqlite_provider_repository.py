from typing import Dict
from sqlalchemy.future import select
from src.infra.sqlite.config import AsyncSession, sessionmaker
from src.infra.sqlite.models.provider import ProviderModel
from src.interactor.repository.provider_repository import ProviderRepositoryInterface


class SqliteProviderRepository(ProviderRepositoryInterface):
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_provider(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item_db = ProviderModel(**payload)
                session.add(item_db)
                session.commit()
                session.refresh(item_db)
                return item_db

    async def get_provider_by_name(self, provider_name: str):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                q = await session.execute(
                    select(ProviderModel).where(
                        ProviderModel.provider_name == provider_name
                    )
                )
                result = q.scalars().first()
                return result

    async def get_all_provider(self):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                q = await session.execute(select(ProviderModel))
                result = q.scalars().all()
                return result
