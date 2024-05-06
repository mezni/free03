from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UUID, Column, String, ForeignKey


Base = declarative_base()


class ProviderModel(Base):
    __tablename__ = "providers"
    provider_code = Column(UUID, primary_key=True, index=True)
    provider_name = Column(String(60), unique=True, nullable=False, index=True)
