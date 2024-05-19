from __future__ import annotations
import uuid
from typing import TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime

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
    
portfolio_input_dto = PortfolioInputDto(portfolio_name="default",portfolio_type="root")
portfolio_data = portfolio_input_dto.model_dump()
portfolio = Portfolio(**portfolio_data)
