import uuid
import asyncio

from src.db_config import init_db, create_db_engine
from src.dtos import OrganisationOutputDto, OrganisationInputDto
from src.repositories import OrganisationRepository


async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)
    org_repo = OrganisationRepository(engine)

    org_dto = OrganisationInputDto(org_name="Eclipse")
    org = await org_repo.create_organisation(org_dto.model_dump())


asyncio.run(main())
