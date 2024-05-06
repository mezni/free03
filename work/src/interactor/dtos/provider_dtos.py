from pydantic import BaseModel
from src.domain.types import generate_uuid, UUIDType
from src.domain.provider import Provider


class ProviderInputDto(BaseModel):
    provider_code: UUIDType = None
    provider_name: str

    def model_post_init(self, __context) -> None:
        self.provider_code = generate_uuid()


class ProviderOutputDto(Provider):

    pass
