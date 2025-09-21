from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class FavoriteModel(Base):
    __tablename__ = "favorite"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_id = Column(
        BigInteger, ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
