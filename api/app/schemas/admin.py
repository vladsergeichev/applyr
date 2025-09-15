from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    telegram_username: str | None = None
    created_at: datetime


class VacancyResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    link: str | None = None
    company_name: str | None = None
    user_id: int
    created_at: datetime


class StageResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    order_index: int
    vacancy_id: int
    created_at: datetime


class TokenResponse(BaseModel):
    id: int
    token_hash: str
    user_id: int
    expires_at: datetime
    created_at: datetime
