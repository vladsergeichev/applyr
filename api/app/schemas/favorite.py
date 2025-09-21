from datetime import datetime

from pydantic import BaseModel


class FavoriteBaseSchema(BaseModel):
    notes: str | None = None


class FavoriteSchema(FavoriteBaseSchema):
    id: int
    user_id: int
    vacancy_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
