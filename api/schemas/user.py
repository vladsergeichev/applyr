from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    name: str
    username: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    id: int  # telegram_id


class UserSchema(UserBaseSchema):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
