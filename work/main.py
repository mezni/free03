import uuid
import asyncio

from src.infra.sqlite.config import create_db_engine, init_db
from src.infra.sqlite.repositories.sqlite_provider_repository import (
    SqliteProviderRepository,
)
from src.interactor.usecases.provider_usecase import ProviderCreateUsecase


async def main():
    db_url = "sqlite+aiosqlite:///_usage.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)
    provider_repo = SqliteProviderRepository(engine)
    #    payload = {"provider_code": uuid.uuid4(), "provider_name": "oci2"}
    #    u=await provider_repo.create_provider(payload)
    #    print (u.__dict__)
    #    x = await provider_repo.get_all_provider()
    #    for i in x:
    #        print(i.__dict__)

    #    x = await provider_repo.get_provider_by_name("aws")
    #    if x:
    #        print(x.__dict__)

    provider_usecase = ProviderCreateUsecase(provider_repo)
    payload = {"provider_code": uuid.uuid4(), "provider_name": "aws"}
    await provider_usecase.create(payload)

asyncio.run(main())
