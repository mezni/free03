from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class SqliteProviderRepository:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=True, future=True)
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_post(self, post):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                session.add(post)

    async def get_all_posts(self):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                return await session.execute(Post.__table__.select()).scalars().all()
