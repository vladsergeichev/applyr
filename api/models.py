import hashlib
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # telegram_id
    username = Column(String(255), nullable=True, unique=True)  # telegram username
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Apply(Base):
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


class ApplyState(Base):
    __tablename__ = "apply_states"

    id = Column(String(64), primary_key=True)  # хэш-идентификатор
    apply_id = Column(
        String(64), ForeignKey("applies.id", ondelete="CASCADE"), nullable=False
    )
    state_id = Column(
        Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(Text)
    occurred_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def generate_id(cls, apply_id: str, state_id: int) -> str:
        """Генерирует хэш-идентификатор для состояния отклика"""
        data = f"{apply_id}_{state_id}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
