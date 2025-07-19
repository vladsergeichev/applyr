from datetime import datetime

from pydantic import BaseModel


class AuthRegisterSchema(BaseModel):
    username: str
    password: str
    name: str


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


class UserInfoSchema(BaseModel):
    id: int
    username: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
