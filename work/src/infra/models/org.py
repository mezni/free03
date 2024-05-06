from sqlalchemy import UUID, Column, String, ForeignKey
from src.infra.base import Base


class OrgModel(Base):
    __tablename__ = "orgs"
    org_code = Column(UUID, primary_key=True, index=True)
    org_name = Column(String(60), unique=True, nullable=False, index=True)
