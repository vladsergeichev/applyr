from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StageBaseSchema(BaseModel):
    vacancy_id: int = Field(..., gt=0, description="ID вакансии")
    stage_type: str = Field(..., min_length=1, max_length=255, description="Тип этапа")
    title: Optional[str] = Field(
        None, max_length=255, description="Название этапа"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание этапа"
    )


class StageCreateSchema(StageBaseSchema):
    created_at: Optional[datetime] = Field(
        None, description="Дата создания этапа"
    )


class StageUpdateSchema(BaseModel):
    stage_type: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Тип этапа"
    )
    title: Optional[str] = Field(
        None, max_length=255, description="Название этапа"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание этапа"
    )


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
