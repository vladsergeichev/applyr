from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.schemas.vacancy import VacancyStatus


class VacancyModel(Base):
    __tablename__ = "vacancy"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # автор вакансии TODO: переименовать в author_id
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(500), nullable=False)
    status = Column(
        ENUM(VacancyStatus, name="vacancy_status"), default=VacancyStatus.DRAFT
    )
    link = Column(Text, nullable=False)
    contact_link = Column(Text)
    company_name = Column(Text)
    salary = Column(Text)
    experience = Column(String(100))
    location = Column(String(200))
    employment = Column(String(100))
    description = Column(Text)
    requirements = Column(Text)
    conditions = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    stages = relationship("StageModel", backref="vacancy", cascade="all, delete-orphan")
