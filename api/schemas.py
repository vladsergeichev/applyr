from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# User schemas
class UserBase(BaseModel):
    name: str
    username: Optional[str] = None


class UserCreate(UserBase):
    id: int  # telegram_id


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Apply schemas
class ApplyBase(BaseModel):
    name: str
    link: str
    description: Optional[str] = None


class ApplyCreate(ApplyBase):
    user_id: int


class ApplyUpdate(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None


class Apply(ApplyBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# State schemas
class StateBase(BaseModel):
    name: str


class StateCreate(StateBase):
    pass


class StateUpdate(BaseModel):
    name: str


class State(StateBase):
    id: int

    class Config:
        from_attributes = True


# ApplyState schemas
class ApplyStateBase(BaseModel):
    state_id: int
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None


class ApplyStateCreate(ApplyStateBase):
    apply_id: str


class ApplyStateUpdate(BaseModel):
    state_id: Optional[int] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None


class ApplyState(ApplyStateBase):
    id: str
    apply_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
