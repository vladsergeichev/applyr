from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.sql import func

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # telegram_id
    username = Column(String(255), nullable=True, unique=True)  # telegram username
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)  # для аутентификации
    created_at = Column(DateTime, default=func.now())
