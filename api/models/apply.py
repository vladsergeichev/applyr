import hashlib
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func

from database import Base


class ApplyModel(Base):
    __tablename__ = "applies"

    id = Column(String(64), primary_key=True)  # хэш-идентификатор
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(500), nullable=False)  # название вакансии
    link = Column(Text, nullable=False)  # ссылка на вакансию
    company_name = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def generate_id(cls, user_id: int, name: str) -> str:
        """Генерирует хэш-идентификатор для отклика"""
        data = f"{user_id}_{name}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
