from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class Team(BaseModel):
    name: str

class UserRegister(BaseModel):
    # These are the only attributes required for registration
    username: str
    email: str
    password: str

class User(BaseModel):
    username: str
    email: str
    password: str

    is_active: bool = False

    created_at: date
    updated_at: date
    last_login: Union[str, None] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
