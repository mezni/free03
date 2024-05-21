import uuid
from pydantic import BaseModel
from typing import TypeVar, Optional, Dict, List
from datetime import datetime, date

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class Portfolio(BaseModel):
    portfolio_code: UUIDType = None
    portfolio_name: str
    portfolio_type: str
    portfolio_parent: Optional[UUIDType] = None

    def model_post_init(self, __context) -> None:
        self.portfolio_code = generate_uuid()


class CostAllocation(BaseModel):
    allocation_code: UUIDType = None
    total_cost: float = 0.0
    effective_date: date
    expiry_date: date
    portfolio_code: UUIDType

    def model_post_init(self, __context) -> None:
        self.portfolio_code = generate_uuid()


class AllocationRepository:
    def __init__(self):
        self.portfolios = []
        self.allocations = []

    def add_portfolio(self, portfolio: Portfolio):
        self.portfolios.append(portfolio)

    def get_portfolio_name(self, portfolio_name: str):
        for p in self.portfolios:
            if p.portfolio_name == portfolio_name:
                return p
        return None

    def get_all_portfolio(self) -> List[Portfolio]:
        return self.portfolios

    def add_allocation(self, allocation: CostAllocation):
        self.allocations.append(allocation)

    def get_all_allocation(self) -> List[CostAllocation]:
        return self.allocations


allocation_repo = AllocationRepository()
allocation_repo.add_portfolio(
    Portfolio(portfolio_name="default", portfolio_type="root")
)
portfolio_default = allocation_repo.get_portfolio_name("default")
allocation_repo.add_allocation(
    CostAllocation(
        total_cost=2000,
        effective_date=date(2024, 1, 1),
        expiry_date=date(2024, 12, 31),
        portfolio_code=portfolio_default.model_dump()["portfolio_code"],
    )
)
allocation_repo.add_portfolio(
    Portfolio(
        portfolio_name="IT",
        portfolio_type="Departement",
        portfolio_parent=portfolio_default.model_dump()["portfolio_code"],
    )
)
allocation_repo.add_portfolio(
    Portfolio(
        portfolio_name="Sales",
        portfolio_type="Departement",
        portfolio_parent=portfolio_default.model_dump()["portfolio_code"],
    )
)

print("# Portfolios")
portfolios = allocation_repo.get_all_portfolio()
for p in portfolios:
    print(p)

print("# Allocations")
allocations = allocation_repo.get_all_allocation()
for a in allocations:
    print(a)
