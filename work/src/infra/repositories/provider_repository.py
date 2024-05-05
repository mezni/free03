from typing import Dict
from src.infra.db_config import AsyncSession, sessionmaker
from src.infra.models.provider import ProviderModel

class ProviderRepository:
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
                return item_db   