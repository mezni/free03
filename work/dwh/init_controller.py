import asyncio
from db_config import init_db, create_db_engine
from repositories import OrganisationRepository, ProviderRepository, PeriodRepository
from dtos import OrganisationInputDto, ProviderInputDto, PeriodInputDTO
from datetime import datetime, date, timedelta


async def execute():
    db_url = "sqlite+aiosqlite:///_store/_dwh.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)

    # Org
    org_repo = OrganisationRepository(engine)
    org_name = "faclon tech"
    org_input = OrganisationInputDto(org_name=org_name)
    org_item = await org_repo.create_organisation(org_input.model_dump())

    # Providers
    provider_repo = ProviderRepository(engine)
    providers = ["aws", "azure", "oci"]
    for provider_name in providers:
        provider_input = ProviderInputDto(provider_name=provider_name)
        provider_item = await provider_repo.create_provider(provider_input.model_dump())

    # Periods
    period_repo = PeriodRepository(engine)
    start_date = date(year=2023, month=9, day=1)
    end_date = date(year=2024, month=9, day=30)
    curr_date = start_date
    while curr_date <= end_date:
        period_name = curr_date.strftime("%Y-%m-%d")
        period_input = PeriodInputDTO(period_name=period_name)
        period_item = await period_repo.create_period(period_input.model_dump())
        curr_date += timedelta(days=1)


asyncio.run(execute())
