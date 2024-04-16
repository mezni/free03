import enum
from sqlalchemy import Column, String, Integer, ForeignKey
from src.infra.db_base import Base


class AnimalTypes(enum.Enum):
    dog = "dog"
    cat = "cat"
    fish = "fish"
    turtle = "turtle"


class Pets(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specie = Column(enum.Enum(AnimalTypes), nullable=False)
    age = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"Users [id={self.id}, name={self.name}, user_id={self.user_id}]"
