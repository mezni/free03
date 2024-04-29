import uuid
import asyncio
import csv
import pandas as pd
from src.db_config import create_db_engine, init_db
from src.dtos import (
    OrganisationInputDto,
    AccountInputDto,
)
from src.repositories import OrganisationRepository, AccountRepository


async def main():
    db_url = "sqlite+aiosqlite:///_costs.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)
    data_file = "tests/aws_data.csv"
    df = pd.read_csv(data_file)
    # clients
    clients = []
    clients_input = df["Client"].unique().tolist()
    org_repo = OrganisationRepository(engine)
    for client in clients_input:
        item = await org_repo.get_organisation_by_name(client)
        if not item:
            org_input = OrganisationInputDto(org_name=client)
            item = await org_repo.create_organisation(org_input.model_dump())
        clients.append(item)
    print(clients)

    # accounts
    org_code = clients[0].org_code
    org_code = uuid.UUID(str(org_code))
    print(org_code)
    accounts = []
    accounts_input = df["SubscriptionName"].unique().tolist()
    account_repo = AccountRepository(engine)
    for account in accounts_input:
        item = await account_repo.get_account_by_name(account)
        if not item:
            account_input = AccountInputDto(
                account_name=str(account), org_code=org_code
            )
            item = await account_repo.create_account(account_input.model_dump())
        accounts.append(item)
    print(accounts)


asyncio.run(main())
