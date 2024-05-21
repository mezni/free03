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


class PortfolioRepository:
    def __init__(self):
        self.portfolios = []

    def add_portfolio(self, portfolio: Portfolio):
        self.portfolios.append(portfolio)

    def get_all_portfolios(self) -> List[Portfolio]:
        return self.portfolios

    def find_portfolio_by_id(self, portfolio_code: UUIDType) -> Optional[Portfolio]:
        return next(
            (
                portfolio
                for portfolio in self.portfolios
                if portfolio.portfolio_code == portfolio_code
            ),
            None,
        )

    def update_portfolio(
        self, portfolio_code: UUIDType, portfolio_name: str, portfolio_type: str
    ) -> Optional[Portfolio]:
        portfolio = self.find_portfolio_by_id(portfolio_code)
        if portfolio:
            portfolio.portfolio_name = portfolio_name
            portfolio.portfolio_type = portfolio_type
        return portfolio


portfolio_usecase = PortfolioRepository()
portfolio_usecase.add_portfolio(
    Portfolio(portfolio_name="default", portfolio_type="root")
)
portfolios=portfolio_usecase.get_all_portfolios()
for p in portfolios:
    print (p)
    x=portfolio_usecase.update_portfolio(p.portfolio_code,"default","defaulta")
    print (x)