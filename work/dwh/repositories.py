from typing import Dict, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from db_config import Base
from models import OrganisationModel, ProviderModel, PeriodModel
from dtos import OrganisationOutputDto, ProviderOutputDto, PeriodOutputtDTO


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
                return to_pydantic(item_db, ProviderOutputDto)


class PeriodRepository:
    def __init__(self, engine):
        self.engine = engine
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_period(self, payload: Dict):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                item_db = PeriodModel(**payload)
                session.add(item_db)
                return to_pydantic(item_db, PeriodOutputtDTO)
