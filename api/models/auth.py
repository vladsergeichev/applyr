from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from database import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    telegram_username = Column(String(255), unique=True)
    created_at = Column(DateTime, default=func.now())


class RefreshModel(Base):
    __tablename__ = "refresh"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    token_hash = Column(String(255), nullable=False)  # хеш refresh токена
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
