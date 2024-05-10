import uuid
import asyncio
from datetime import date, timedelta
from db_config import init_db, create_db_engine
from sqlalchemy.orm import sessionmaker
from models import OrganisationModel, ProviderModel
from sqlalchemy.ext.asyncio import AsyncSession


def date_range_list(start_date, end_date):
    # Return list of datetime.date objects (inclusive) between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += timedelta(days=1)
    return date_list

async def create_orgs(engine):
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_org = OrganisationModel(org_code=uuid.uuid4(),org_name="falcon tech")
            session.add(new_org)


async def create_providers(engine):
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for provider_name in ["aws","azure","oci"]:
                provider_org = ProviderModel(provider_code=uuid.uuid4(),provider_name=provider_name)
                session.add(provider_org)
async def main():
    db_url = "sqlite+aiosqlite:///_dwh.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)
#    await create_orgs(engine)
#    await create_providers(engine)
    
    start_date = date(year=2023, month=9, day=1)
    stop_date = date(year=2024, month=9, day=1)
    date_list = date_range_list(start_date, stop_date)


asyncio.run(main())
