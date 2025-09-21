from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class FavoriteStage(Enum):
    NOTHING = "nothing"
    APPLY_SENT = "apply_sent"
    HR_INTERVIEW = "hr_interview"
    TECH_INTERVIEW = "tech_interview"
    BUSINESS_INTERVIEW = "business_interview"
    WAITING_FEEDBACK = "waiting_feedback"
    REJECTED = "rejected"
    OFFER_RECEIVED = "offer_received"
    ARCHIVE = "archive"
    # NOTHING = "Новая вакансия"
    # APPLY_SENT = "Отклик отправлен"
    # HR_INTERVIEW = "HR собес"
    # TECH_INTERVIEW = "Тех. собес"
    # BUSINESS_INTERVIEW = "Бизнес-собес"
    # WAITING_FEEDBACK = "Ожидание ОС"
    # REJECTED = "Отказ"
    # OFFER_RECEIVED = "Получен оффер"
    # ARCHIVE = "Архив"


class FavoriteBaseSchema(BaseModel):
    stage: FavoriteStage = FavoriteStage.NOTHING
    notes: str | None = None

    class Config:
        from_attributes = True


class FavoriteSchema(FavoriteBaseSchema):
    id: int
    user_id: int
    vacancy_id: int
    created_at: datetime
    updated_at: datetime
