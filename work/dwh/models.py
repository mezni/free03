from sqlalchemy import UUID, Column, Integer, String, ForeignKey


from db_base import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"
    org_code = Column(UUID, primary_key=True, index=True)
    org_name = Column(String(60), unique=True, nullable=False, index=True)

class ProviderModel(Base):
    __tablename__ = "providers"
    provider_code = Column(UUID, primary_key=True, index=True)
    provider_name = Column(String(60), unique=True, nullable=False, index=True)