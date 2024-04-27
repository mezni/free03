from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict
from sqlalchemy.future import select
from src.infra.sqlite.models.provider import ProviderModel


class SqliteProviderRepository:
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_provider(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item = ProviderModel(**payload)
                session.add(item)

    async def get_all_provider(self):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                q = await session.execute(select(ProviderModel))
                result = q.scalars().all()
                return result


#    async def create_provider(self, payload):
#        async with self.AsyncSessionLocal() as session:
#            async with session.begin():
#                session.add(payload)

#    async def get_all_provider(self):
#        async with self.AsyncSessionLocal() as session:
#            async with session.begin():
#                return await session.execute(Post.__table__.select()).scalars().all()
