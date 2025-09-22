from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from app.schemas.favorite import FavoriteStage


class VacancyStatus(Enum):
    DRAFT = "draft"
    MODERATION = "moderation"
    PUBLISHED = "published"
    EXPIRED = "expired"


class VacancyBaseSchema(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=500, description="Название вакансии"
    )
    status: VacancyStatus = Field(VacancyStatus.DRAFT, description="Статус вакансии")
    link: str = Field(..., min_length=1, description="Ссылка на вакансию")
    contact_link: str | None = Field(None, description="Ссылка на контактное лицо")
    company_name: str | None = Field(
        None, max_length=255, description="Название компании"
    )
    salary: str | None = Field(None, description="Уровень дохода")
    experience: str | None = Field(None, max_length=100, description="Опыт работы")
    location: str | None = Field(None, max_length=200, description="Локация")
    employment: str | None = Field(None, max_length=100, description="Тип занятости")
    description: str | None = Field(None, description="Описание")
    requirements: str | None = Field(None, description="Требования к кандидату")
    conditions: str | None = Field(None, description="Условия работы")

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return v.strip() if v else v

    @field_validator("link")
    def validate_link(cls, v):
        if v is not None:
            link = v.strip()
            if not link:
                raise ValueError("Ссылка не может быть пустой")
            if "." not in link:
                raise ValueError("Неверный формат ссылки")
            if not link.startswith(("http://", "https://")):
                link = "https://" + link
            return link
        return v


class VacancyCreateSchema(VacancyBaseSchema):
    user_id: int = Field(..., gt=0, description="ID пользователя")

    @field_validator("user_id")
    def validate_user_id(cls, v):
        if v <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")
        return v


class VacancyUpdateSchema(VacancyBaseSchema):
    pass


class VacancySchema(VacancyBaseSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GetVacancySchema(VacancyBaseSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    notes: str | None = None
    stage: FavoriteStage = FavoriteStage.NOTHING

    class Config:
        from_attributes = True
