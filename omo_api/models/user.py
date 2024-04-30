from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class Team(BaseModel):
    name: str

    class Config:
        orm_mode = True

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

class Account(BaseModel):
    type: str
    provider: str
    provider_account_id: str
    refresh_token: Union[str, None] = None
    access_token: Union[str, None] = None
    expires_at: Union[int, None] = None
    id_token: Union[str, None] = None
    scope: Union[str, None] = None
    session_state: Union[str, None] = None
    token_type: Union[str, None] = None

    class Config:
        orm_mode = True

class UserRegistration(BaseModel):
    email: str
    # these are optional in the case of social logins
    username: Union[str, None] = None
    password: Union[str, None] = None
    slackCode: Union[str, None] = None


class UserAccountRegistration(UserRegistration, Account):
    name: str

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

class ConnectorContext(BaseModel):
    name: str
    id: List[int]

class UserContext(BaseModel):
    id: int
    email: str
    updated_at: str
    is_active: bool
    team_id: int
    created_at: datetime
    connectors: List[ConnectorContext]
    vector_store: VectorStoreContext


