""" Usage dtos module
"""

from pydantic import BaseModel
from src.entities import Provider, UUIDType, generate_uuid


class ProviderInputDto(BaseModel):
    """Definition of the ProviderInputDTO"""

    provider_code: UUIDType = None
    provider_name: str

    def model_post_init(self, __context) -> None:
        self.provider_code = generate_uuid()


class ProviderOutputtDto(Provider):
    """Definition of the ProviderOutputtDTO"""

    pass
