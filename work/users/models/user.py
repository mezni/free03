from sqlalchemy import UUID, Column, String, ForeignKey
from src.infra.db_base import Base


class UserModel(Base):
    __tablename__ = "users"
    user_code = Column(UUID, primary_key=True, index=True)
    user_name = Column(String(60), unique=True, nullable=False, index=True)
    user_email = Column(String(60), unique=True, nullable=False, index=True)
    user_password = Column(String(60), unique=True, nullable=False, index=True)
