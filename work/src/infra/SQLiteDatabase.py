from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.infra.base import Base


class SQLiteDatabase:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)

    async def get_session(self):
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
