from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from app.database import Base
from app.schemas.favorite import FavoriteStage


class FavoriteModel(Base):
    __tablename__ = "favorite"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    vacancy_id = Column(
        BigInteger, ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    stage = Column(
        ENUM(FavoriteStage, name="favorite_stage"), default=FavoriteStage.NOTHING
    )

    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
