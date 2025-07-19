from sqlalchemy import Column, Integer, String

from database import Base


class StateModel(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
