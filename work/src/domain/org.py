from datetime import datetime
from pydantic import BaseModel
from src.domain.types import UUIDType


class Org(BaseModel):

    org_code: UUIDType
    org_name: str
