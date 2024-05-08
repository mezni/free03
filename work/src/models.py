from sqlalchemy import UUID, Column, String, ForeignKey


from src.db_base import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"
    org_code = Column(UUID, primary_key=True, index=True)
    org_name = Column(String(60), unique=True, nullable=False, index=True)


class AccountModel(Base):
    __tablename__ = "accounts"
    account_code = Column(UUID, primary_key=True, index=True)
    account_name = Column(String(60), unique=True, nullable=False, index=True)
    org_code = Column(UUID, ForeignKey("organisations.org_code"), index=True)
