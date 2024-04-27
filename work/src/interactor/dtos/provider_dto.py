from pydantic import BaseModel
from src.domain.value_objects import UUIDType, generate_uuid
from src.domain.provider import Provider


class ProviderInputDto(BaseModel):
    provider_code: UUIDType = None
    provider_name: str

    def model_post_init(self, __context) -> None:
        self.provider_code = generate_uuid()


class ProviderOutputtDto(Provider):

    pass
