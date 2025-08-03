from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from schemas.stage import GetStageSchema

class VacancyBaseSchema(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=500, description="Название вакансии"
    )
    link: str = Field(..., min_length=1, description="Ссылка на вакансию")
    company_name: Optional[str] = Field(
        None, max_length=255, description="Название компании"
    )
    description: Optional[str] = Field(None, max_length=1000, description="Описание")

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return v.strip()

    @field_validator("link")
    def validate_link(cls, v):
        if not v.strip():
            raise ValueError("Ссылка не может быть пустой")
        try:
            result = urlparse(v)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Неверный формат ссылки")
        except Exception:
            raise ValueError("Неверный формат ссылки")
        return v.strip()


class VacancyCreateSchema(VacancyBaseSchema):
    user_id: int = Field(..., gt=0, description="ID пользователя")

    @field_validator("user_id")
    def validate_user_id(cls, v):
        if v <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")
        return v


class VacancyUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=500, description="Название вакансии"
    )
    link: Optional[str] = Field(None, min_length=1, description="Ссылка на вакансию")
    company_name: Optional[str] = Field(
        None, max_length=255, description="Название компании"
    )
    description: Optional[str] = Field(None, max_length=1000, description="Описание")

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return v.strip() if v else v

    @field_validator("link")
    def validate_link(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Ссылка не может быть пустой")
            try:
                result = urlparse(v)
                if not all([result.scheme, result.netloc]):
                    raise ValueError("Неверный формат ссылки")
            except Exception:
                raise ValueError("Неверный формат ссылки")
            return v.strip()
        return v


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
    stages: list[GetStageSchema]
