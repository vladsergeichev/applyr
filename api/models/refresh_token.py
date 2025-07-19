import hashlib
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from database import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String(64), primary_key=True)  # хэш-идентификатор токена
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_hash = Column(String(255), nullable=False)  # хеш refresh токена
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

    @classmethod
    def generate_id(cls, user_id: int) -> str:
        """Генерирует хэш-идентификатор для refresh токена"""
        data = f"{user_id}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
