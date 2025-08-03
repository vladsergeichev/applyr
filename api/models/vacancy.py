from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class VacancyModel(Base):
    __tablename__ = "vacancy"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(500), nullable=False)
    link = Column(Text, nullable=False)
    company_name = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    stages = relationship("StageModel", backref="vacancy", cascade="all, delete-orphan")
