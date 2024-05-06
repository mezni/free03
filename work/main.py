import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.infra.adapters.provider_repository import SQLiteProviderRepository
from src.interactor.usecases.provider_usecase import AddProviderUseCase
from src.app.controllers.provider_controller import ProviderController
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


async def init_db(db_url: str):
    engine = create_async_engine(db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return async_session


async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    async_session = await init_db(db_url)

    provider_repo = SQLiteProviderRepository(async_session)
    add_provider_usecase = AddProviderUseCase(provider_repo)
    provider_controller = ProviderController(add_provider_usecase)

    # Add a user
    provider = await provider_controller.add_provider("Alice")
    print("User added:", provider)


if __name__ == "__main__":
    asyncio.run(main())
