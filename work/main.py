import uuid
import asyncio

from src.infra.sqlite.config import create_db_engine, init_db
from src.infra.sqlite.repositories.sqlite_provider_repository import (
    SqliteProviderRepository,
)


async def main():
    db_url = "sqlite+aiosqlite:///_usage.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)
    provider_repo = SqliteProviderRepository(engine)
    payload = {"provider_code": uuid.uuid4(), "provider_name": "oci"}
    await provider_repo.create_provider(payload)
    x = await provider_repo.get_all_provider()
    for i in x:
        print(i.provider_code, i.provider_name)


asyncio.run(main())
