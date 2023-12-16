import os
import logging
import pinecone
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, status, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.sql import func
from omo_api.models.google_drive import GoogleDriveObjects, GoogleDriveObject
from omo_api.db.utils import get_db
from omo_api.db.models.googledrive import GDriveObject
from langchain_googledrive.document_loaders import GoogleDriveLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from omo_api.db.models.user import User
from omo_api.models.user import UserRegister, Token
from omo_api.utils.auth import get_password_hash, authenticate_user, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 60*60*24

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

@router.post('/v1/auth/user/login', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    logger.debug('form data*****', form_data)
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}