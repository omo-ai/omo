import logging

from typing import Union, Annotated
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Security, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import botocore 
import botocore.session 
from botocore.exceptions import ClientError
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 
from google.oauth2 import id_token
from google.auth.transport import requests

from omo_api.utils import get_env_var
from omo_api.db.utils import get_db
from omo_api.db.models.user import User
from omo_api.models.user import JWTTokenData


AUTH_SECRET = get_env_var('AUTH_SECRET')
ALGORITHM = 'HS256'

http_bearer = HTTPBearer(auto_error=True)
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__) #

def verify_password(cleartext_pw: str, hashed_pw: str) -> bool:
    return crypt_context.verify(cleartext_pw, hashed_pw)

def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET, algorithm=ALGORITHM)
    return encoded_jwt
    

def authenticate_user(email: str, password: str, db: Session) -> bool:

    stmt = select(User.email, User.hashed_password) \
            .where(User.email == email) \
            .where(User.is_active == True)

    result = db.execute(stmt)
    user = result.fetchone()

    if not user:
        return False
     
    if verify_password(password, user.hashed_password):
        return user

    return False

def get_user(db: Session, email: str) -> User:

    try:
        stmt = select(
            User.id,
            User.email,
            User.is_active,
            User.created_at).filter(User.email == email)

        result = db.execute(stmt)
        row = result.one_or_none()
        return row

    except MultipleResultsFound as e:
        logger.debug("get_user: user does not exist")
        return None        


def parse_jwt_sub(value: str) -> str:
    if ':' in value:
        return value.split[':'][1]
    
    return value

# async def get_current_user(token: HTTPAuthorizationCredentials = Depends(http_bearer),
#                            db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         logger.debug(token)
#         payload = jwt.decode(token.credentials, AUTH_SECRET, algorithms=[ALGORITHM])
#         email: str = parse_jwt_sub(payload.get("sub"))
#         if email is None:
#             raise credentials_exception
#         token_data = JWTTokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     #logger.debug('get_active_current_user', current_user.email)
#     return current_user



def get_aws_secret(secret_name: str, region: str='us-west-2'):
    secret = None
    client = botocore.session.get_session().create_client('secretsmanager', region_name=region)
    try:
        cache_config = SecretCacheConfig()
        cache = SecretCache( config = cache_config, client = client)
        secret = cache.get_secret_string(secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        logger.debug(f"Error getting secret: {e}")
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    return secret

