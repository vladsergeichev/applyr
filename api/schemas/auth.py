import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AuthRegisterSchema(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username пользователя"
    )
    password: str = Field(
        ..., min_length=6, max_length=100, description="Пароль пользователя"
    )

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Username должен содержать только буквы, цифры и подчеркивания"
            )
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return v


class AuthLoginSchema(BaseModel):
    username: str
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataSchema(BaseModel):
    user_id: int
    username: str


class AuthResultSchema(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    username: str


class UpdateTelegramSchema(BaseModel):
    telegram_username: str = Field(..., min_length=1, max_length=50)


class UserInfoSchema(BaseModel):
    id: int
    username: str
    telegram_username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
