from sqlalchemy import UUID, Column, String, ForeignKey


from src.infra.db_base import Base


class ProviderModel(Base):
    __tablename__ = "providers"
    provider_code = Column(UUID, primary_key=True, index=True)
    provider_name = Column(String(60), unique=True, nullable=False, index=True)
