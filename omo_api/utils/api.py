import secrets
import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Security, Depends
from fastapi import Depends, status, HTTPException 
from fastapi.security import APIKeyHeader
from omo_api.db.utils import get_db
from omo_api.db.models import APIKey

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key")

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_api_key(length: int = 32) -> str:
    return secrets.token_hex(length)

def get_api_key_hash(api_key: str) -> str:
    return crypt_context.hash(api_key)

def verify_api_key(hashed_key: str, plaintext_key: str) -> bool:
    return crypt_context.verify(plaintext_key, hashed_key)

async def valid_api_token(api_key = Depends(api_key_header), db: Session = Depends(get_db)):
    try:
        hashed_key = get_api_key_hash(api_key)
        stmt = select(APIKey)\
                .where(APIKey.hashed_api_key == hashed_key)\
                .where(APIKey.is_active == True)
        result = db.execute(stmt).one_or_none()
        return result

    except Exception as e:
        logger.error(f"Exception in valid_api_token: {e}")
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
        )
