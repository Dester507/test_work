from typing import Literal, Optional, List
from datetime import datetime

from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class TokenSchema(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    full_name: str
    age: Optional[int] = None
    scopes: List[str]
    created_at: datetime

    class Config:
        orm_mode = True


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    full_name: str
    age: Optional[int] = None
