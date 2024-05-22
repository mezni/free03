from base_entity import BaseDomainModel
from typing import TypeVar, Optional, Dict, List


class Role(BaseDomainModel):
    name: str
    description: Optional[str] = None
