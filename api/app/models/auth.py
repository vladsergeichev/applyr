from enum import Enum

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from app.database import Base


class Roles(Enum):
    user = "user"
    admin = "admin"


class UserModel(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)
    role = Column(ENUM(Roles), default=Roles.user)
    telegram_username = Column(String(255), unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class RefreshModel(Base):
    __tablename__ = "refresh"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
