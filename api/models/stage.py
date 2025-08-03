from enum import Enum

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from database import Base


class StageTypes(Enum):
    NEW = "new"
    HR = "hr"
    TECH = "tech"
    BUSINESS = "business"
    REJECTED = "rejected"
    OFFER = "offer"


# На будущее, для перехода на подробную sate-машину
# class StatusEnum(Enum):
#     NEW = "Новая вакансия"
#     APPLY_SENT = "Отклик отправлен"  # Ожидание ответа от HR
#     HR_INTERVIEW = "Собеседование с HR"
#     WAITING_HR_FEEDBACK = "Ожидание обратной связи от HR"
#     TECH_INTERVIEW = "Техническое собеседование"
#     WAITING_TECH_FEEDBACK = "Ожидание обратной связи о техническом собеседовании"
#     BUSINESS_INTERVIEW = "Собеседование с бизнесом"
#     WAITING_BUSINESS_FEEDBACK = "Ожидание обратной связи о бизнес-собеседовании"
#     WAITING_RESULT = "Ожидание итогового ответа"
#     REJECTED = "Отказ"
#     OFFER_RECEIVED = "Получен оффер"


class StageModel(Base):
    __tablename__ = "stage"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_id = Column(
        BigInteger, ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False
    )
    stage_type = Column(ENUM(StageTypes), default=StageTypes.NEW)
    title = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
