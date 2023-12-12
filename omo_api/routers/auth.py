import os
import logging
import pinecone
from fastapi import Depends, APIRouter
from typing import List, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.sql import func
from models.GoogleDrive import GoogleDriveObjects, GoogleDriveObject
from db.utils import get_db
from db.models.googledrive import GDriveObject
from langchain_googledrive.document_loaders import GoogleDriveLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from db.models.user import User
from models.user import UserRegister
from utils.auth import get_password_hash

# since environment variable it's a relative to the root of the project, not this file
os.environ['GOOGLE_ACCOUNT_FILE'] = './routers/google_service_key.json'

logger = logging.getLogger(__name__) 

router = APIRouter()
@router.post('/v1/auth/user/register')
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    # TODO can probably use get_or_create method here
    logger.debug('registering user...')
    stmt = select(User.email, User.username).where(User.email == user.email)

    try:
        result = db.execute(stmt)
        row = result.one_or_none()
    except MultipleResultsFound as e:
        msg = {'error': 'Email already registered.'}
        logger.debug("register: user already exists")
        return msg

    user_attr = {
        'email': user.email,
        'username': user.username,
        'hashed_password': get_password_hash(user.password),
        'is_active': False,
    }

    new_user = User(**user_attr)
    db.add(new_user)
    db.commit()

    logger.debug('created new user %s' % user.email)

    msg = {'message': 'Account created.'}

    return msg