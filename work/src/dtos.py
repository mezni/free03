import uuid
from pydantic import BaseModel
from src.entities import UUIDType, Organisation, Account


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class OrganisationInputDto(BaseModel):
    org_code: UUIDType = None
    org_name: str

    def model_post_init(self, __context) -> None:
        self.org_code = generate_uuid()


class OrganisationOutputDto(Organisation):

    pass


class AccountInputDto(BaseModel):
    account_code: UUIDType = None
    account_name: str
    org_code: UUIDType

    def model_post_init(self, __context) -> None:
        self.account_code = generate_uuid()


class AccountOutputDto(Account):

    pass
