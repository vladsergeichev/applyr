from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplyStateBaseSchema(BaseModel):
    state_id: int
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None


class ApplyStateCreateSchema(ApplyStateBaseSchema):
    apply_id: str


class ApplyStateUpdateSchema(BaseModel):
    state_id: Optional[int] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None


class ApplyStateSchema(ApplyStateBaseSchema):
    id: str
    apply_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
