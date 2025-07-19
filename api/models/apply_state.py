import hashlib
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class ApplyStateModel(Base):
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
