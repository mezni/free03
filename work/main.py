import asyncio
import uuid
from typing import TypeVar
from datetime import datetime
from pydantic import BaseModel
from abc import ABC, abstractmethod
from tinydb import TinyDB, Query


UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class Provider(BaseModel):
    provider_code: str
    provider_name: str


class CatalogRepository(ABC):
    @abstractmethod
    def create_provider(self, post):
        pass


class TinyDBCatalogRepository(CatalogRepository):
    def __init__(self, db_path):
        self.db = TinyDB(db_path)
        self.providers_table = self.db.table("providers")

    def create_provider(self, provider):
        self.providers_table.insert(
            {
                "provider_code": provider.provider_code,
                "provider_name": provider.provider_name,
            }
        )


class CatalogInteractor:
    def __init__(self, catalog_repo):
        self.catalog_repo = catalog_repo

    def create_provider(self, provider_name):
        code = generate_uuid()
        provider = Provider(provider_code=str(code), provider_name=provider_name)
        self.catalog_repo.create_provider(provider)


async def main():
    catalog_repo = TinyDBCatalogRepository("_catalog.json")
    catalog_interactor = CatalogInteractor(catalog_repo)
    catalog_interactor.create_provider(provider_name="aws")
    catalog_interactor.create_provider(provider_name="azure")


asyncio.run(main())
