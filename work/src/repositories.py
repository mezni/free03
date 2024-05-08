from typing import Dict, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db_config import Base
from src.models import OrganisationModel, AccountModel
from src.dtos import (
    OrganisationOutputDto,
    AccountOutputDto,
)


T = TypeVar("T", bound=BaseModel)


def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)


class OrganisationRepository:
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_organisation(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item_db = OrganisationModel(**payload)
                session.add(item_db)
                return to_pydantic(item_db, OrganisationOutputDto)

    async def get_organisation_by_name(self, org_name: str):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                q = await session.execute(
                    select(OrganisationModel).where(
                        OrganisationModel.org_name == org_name
                    )
                )
                item_db = q.scalars().first()
                if item_db:
                    return to_pydantic(item_db, OrganisationOutputDto)
                else:
                    return item_db


class AccountRepository:
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_account(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item_db = AccountModel(**payload)
                session.add(item_db)
                return to_pydantic(item_db, AccountOutputDto)

    async def get_account_by_name(self, account_name: str):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                q = await session.execute(
                    select(AccountModel).where(
                        AccountModel.account_name == account_name
                    )
                )
                item_db = q.scalars().first()
                if item_db:
                    return to_pydantic(item_db, AccountOutputDto)
                else:
                    return item_db
