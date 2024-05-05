import uuid
import asyncio
from src.infra.db_config import SQLiteDatabaseAdapter
from src.infra.repositories.provider_repository import ProviderRepository
async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    sql_adapter = SQLiteDatabaseAdapter(db_url)
    await sql_adapter.init_db()
    engine = await sql_adapter.get_engine()
    provider_repo=ProviderRepository(engine)
    await provider_repo.create_provider({"provider_code": uuid.uuid4(), "provider_name": "AWS"})

asyncio.run(main())
