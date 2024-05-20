from __future__ import annotations
import uuid
from typing import TypeVar, Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime, date

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class Portfolio(BaseModel):
    portfolio_code: UUIDType
    portfolio_name: str
    portfolio_type: str
    portfolio_parent: Optional[UUIDType]


class PortfolioInputDto(BaseModel):
    portfolio_code: UUIDType = None
    portfolio_name: str
    portfolio_type: str
    portfolio_parent: UUIDType = None

    def model_post_init(self, __context) -> None:
        self.portfolio_code = generate_uuid()


class PortfolioUsecase:
    def __init__(self) -> None:
        pass

    def addPortfolio(self, payload: Dict) -> Portfolio:
        item = Portfolio(**payload)
        return item

    def addAllocation(self, payload: Dict) -> CostAllocation:
        item = CostAllocation(**payload)
        return item


class CostAllocation(BaseModel):
    allocation_code: UUIDType
    allocation_amount: float
    allocation_date: date
    portfolio_code: UUIDType


if __name__ == "__main__":
    portfolio_usecase = PortfolioUsecase()
    portfolio_input_dto = PortfolioInputDto(
        portfolio_name="default", portfolio_type="root"
    )
    portfolio = portfolio_usecase.addPortfolio(portfolio_input_dto.model_dump())
    print(portfolio.model_dump())
