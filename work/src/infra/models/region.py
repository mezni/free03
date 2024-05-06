from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, String, ForeignKey
from src.infra.base import Base


class RegionModel(Base):
    __tablename__ = "providers"
    region_code = Column(UUID, primary_key=True, index=True)
    region_name = Column(String(60), unique=True, nullable=False, index=True)
    provider_code = Column(UUID, ForeignKey("providers.provider_code"), index=True)
