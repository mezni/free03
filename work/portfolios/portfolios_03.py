import uuid
from pydantic import BaseModel
from typing import TypeVar, Optional, Dict, List
from datetime import datetime, date

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class BaseDomainModel(BaseModel):
    code: UUIDType = generate_uuid()


#    class Config:
#        orm_mode = True


class Portfolio(BaseDomainModel):
    portfolio_name: str
    portfolio_type: str
    portfolio_parent: Optional[UUIDType] = None


class CostAllocation(BaseDomainModel):
    allocation_amount: float = 0.0
    allocation_date: date
    portfolio_code: UUIDType


class AllocationRepository:
    def __init__(self):
        self.portfolios = []

    def add_portfolio(self, portfolio: Portfolio):
        self.portfolios.append(portfolio)

    def get_all_portfolio(self) -> List[Portfolio]:
        return self.portfolios


portfolio_default = Portfolio(portfolio_name="default", portfolio_type="root")
portfolio_it = Portfolio(
    portfolio_name="IT",
    portfolio_type="department",
    portfolio_parent=portfolio_default.model_dump()["code"],
)
portfolio_sales = Portfolio(
    portfolio_name="Sales",
    portfolio_type="department",
    portfolio_parent=portfolio_default.model_dump()["code"],
)
portfolio_phenix = Portfolio(
    portfolio_name="Phenix",
    portfolio_type="project",
    portfolio_parent=portfolio_it.model_dump()["code"],
)
portfolio_inventory = Portfolio(
    portfolio_name="Inventory",
    portfolio_type="project",
    portfolio_parent=portfolio_it.model_dump()["code"],
)
