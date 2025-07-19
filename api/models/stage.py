from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func

from database import Base


class StageModel(Base):
    __tablename__ = "stage"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    apply_id = Column(
        BigInteger, ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    state_type = Column(String(255))
    description = Column(Text)
    occurred_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
