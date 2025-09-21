from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StageTypes(Enum):
    NEW = "new"
    HR = "hr"
    TECH = "tech"
    BUSINESS = "business"
    REJECTED = "rejected"
    OFFER = "offer"


# На будущее, для перехода на подробную state-машину
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


class StageBaseSchema(BaseModel):
    vacancy_id: int = Field(..., gt=0, description="ID вакансии")
    stage_type: str = Field(..., min_length=1, max_length=255, description="Тип этапа")
    title: str | None = Field(None, max_length=255, description="Название этапа")
    description: str | None = Field(None, description="Описание этапа")


class StageCreateSchema(StageBaseSchema):
    created_at: datetime | None = Field(None, description="Дата создания этапа")


class StageUpdateSchema(BaseModel):
    stage_type: str | None = Field(
        None, min_length=1, max_length=255, description="Тип этапа"
    )
    title: str | None = Field(None, max_length=255, description="Название этапа")
    description: str | None = Field(None, description="Описание этапа")


class StageSchema(StageBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GetStageSchema(BaseModel):
    id: int
    stage_type: str
    title: str | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime
