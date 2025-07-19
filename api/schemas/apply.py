from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplyBaseSchema(BaseModel):
    name: str
    link: str
    company_name: Optional[str] = None
    description: Optional[str] = None


class ApplyCreateSchema(ApplyBaseSchema):
    user_id: int


class ApplyUpdateSchema(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None


class ApplySchema(ApplyBaseSchema):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
