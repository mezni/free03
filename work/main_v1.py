import asyncio
from src.load_costs_repository import LoadCostsRepository
from src.load_costs_usecase import LoadCostsUseCase
from pydantic import BaseModel



class CostRecord(BaseModel):
    org_name: str
    provider_name: str

async def main():
    db_url = "sqlite+aiosqlite:///_costs.db"
    aws_mapping = {
        'org_name': 'Client',
        'provider_name': 'Provider'
    }
#    DATA_SOURCE = "csv"  # List
#    SOURCE_PATH = "csv"
#    costs_repo = LoadCostsRepository()
#    costs_usecase = LoadCostsUseCase(costs_repo)
#    data = costs_usecase.process(DATA_SOURCE, SOURCE_PATH)
#    print(data)


asyncio.run(main())
