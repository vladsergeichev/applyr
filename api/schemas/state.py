from pydantic import BaseModel


class StateBaseSchema(BaseModel):
    name: str


class StateCreateSchema(StateBaseSchema):
    pass


class StateUpdateSchema(BaseModel):
    name: str


class StateSchema(StateBaseSchema):
    id: int

    class Config:
        from_attributes = True
