from sqlalchemy import UUID, Column, Integer, String, Date, Boolean, ForeignKey


from db_base import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"
    org_code = Column(UUID, primary_key=True, index=True)
    org_name = Column(String(60), unique=True, nullable=False, index=True)


class ProviderModel(Base):
    __tablename__ = "providers"
    provider_code = Column(UUID, primary_key=True, index=True)
    provider_name = Column(String(60), unique=True, nullable=False, index=True)


class PeriodModel(Base):
    __tablename__ = "periods"
    period_code = Column(UUID, primary_key=True, index=True)
    period_name = Column(String(60), unique=True, nullable=False, index=True)
    period_date = Column(Date, unique=True, nullable=False)
    period_day = Column(Integer, nullable=False)
    period_month = Column(Integer, nullable=False)
    period_year = Column(Integer, nullable=False)
    period_quarter = Column(Integer, nullable=False)
    period_day_of_week = Column(Integer, nullable=False)
    period_day_of_year = Column(Integer, nullable=False)
    period_week_of_year = Column(Integer, nullable=False)
    period_is_holiday = Column(Boolean, nullable=False)
