from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    telegram_username: Optional[str] = None
    created_at: datetime


class VacancyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    company_name: Optional[str] = None
    user_id: int
    created_at: datetime


class StageResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    order_index: int
    vacancy_id: int
    created_at: datetime


class TokenResponse(BaseModel):
    id: int
    token_hash: str
    user_id: int
    expires_at: datetime
    created_at: datetime
