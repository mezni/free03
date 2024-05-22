from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class BaseDomainModel(BaseModel):
    code: UUID = Field(default_factory=uuid4)


#    class Config:
#        orm_mode = True
