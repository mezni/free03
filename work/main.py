import uuid
import asyncio
from src.infra.SQLiteDatabase import SQLiteDatabase
from src.infra.adapters.provider_repository import SQLiteProviderRepository
from src.interactor.usecases.provider_usecase import AddProviderUseCase
from src.app.controllers.provider_controller import ProviderController


async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    sql_db = SQLiteDatabase(db_url)
    await sql_db.init_db()
    async_session = await sql_db.get_session()
    provider_repo = SQLiteProviderRepository(async_session)
    payload = {"provider_code": uuid.uuid4(), "provider_name": "AWS"}
    ret = await provider_repo.add_provider(payload)
    print(ret)


#    provider_repo = SQLiteProviderRepository(async_session)
#    add_provider_usecase = AddProviderUseCase(provider_repo)
#    provider_controller = ProviderController(add_provider_usecase)

# Add a user
#    provider = await provider_controller.add_provider("Alice")
#    print("User added:", provider)


if __name__ == "__main__":
    asyncio.run(main())
