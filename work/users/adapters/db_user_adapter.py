from typing import Dict
from sqlalchemy.future import select
from src.infra.sqlite.config import AsyncSession, sessionmaker
from src.models.user import UserModel
from users.repositories.user_repository import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item_db = UserModel(**payload)
                session.add(item_db)
                session.commit()
                session.refresh(item_db)
                return item_db
