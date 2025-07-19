from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StageBaseSchema(BaseModel):
    apply_id: int = Field(..., gt=0, description="ID вакансии")
    state_type: str = Field(..., min_length=1, max_length=255, description="Тип этапа")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание этапа"
    )
    occurred_at: Optional[datetime] = Field(None, description="Дата наступления этапа")


class StageCreateSchema(StageBaseSchema):
    pass


class StageUpdateSchema(BaseModel):
    state_type: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Тип этапа"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание этапа"
    )
    occurred_at: Optional[datetime] = Field(None, description="Дата наступления этапа")


class StageSchema(StageBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
