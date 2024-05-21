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


class AllocationService:
    pass


# add_portfolio(name,limit,portfolio_type,extend_parent_limit,parent,effective_date,expiry_date)

portfolio_default = portfolio_usecase.create_portfolio(
    portfolio_name="default", portfolio_type="root"
)
portfolio_it = portfolio_usecase.create_portfolio(
    portfolio_name="default",
    portfolio_type="root",
    portfolio_parent=portfolio_default.portfolio_code,
)
