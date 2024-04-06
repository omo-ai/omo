from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class Team(BaseModel):
    name: str

class UserRegister(BaseModel):
    email: str
    # these are optional in the case of social logins
    username: Union[str, None] = None
    password: Union[str, None] = None
    slackCode: Union[str, None] = None

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
    email: str

class TokenData(BaseModel):
    username: str

class VectorStoreContext(BaseModel):
    id: int
    index_name: str
    environment: str
    namespaces: list[str]
    created_at: datetime
    updated_at: datetime
    provider: str

class UserContext(BaseModel):
    email: str
    updated_at: str
    is_active: bool
    team_id: int
    created_at: datetime
    connectors: list
    vector_store: VectorStoreContext
