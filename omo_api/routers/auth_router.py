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
from omo_api.models.user import UserRegister, Token
from omo_api.db.models import User, SlackProfile
from omo_api.utils.auth import get_password_hash, authenticate_user, create_access_token
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

ACCESS_TOKEN_EXPIRE_MINUTES = 60*60*24

logger = logging.getLogger(__name__) 

router = APIRouter()

SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')

def get_oauth_v2_response(temp_auth_code: str, client: WebClient):
    try:
        response = client.oauth_v2_access(
            client_id=SLACK_CLIENT_ID,
            client_secret=SLACK_CLIENT_SECRET,
            code=temp_auth_code,
        )
        logger.debug("oauth2 response", response)

        return response

    except SlackApiError as e:
        logger.debug(f"slack api error: {e}")
        return None

def get_slack_user_info(token: str, slack_user_id: str, client: WebClient):
    try:
        info = client.users_profile_get(token=token, user=slack_user_id)
        return info
    except SlackApiError as e: 
        logger.debug(f"slack api error: {e}")
        return None

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

    if user.slackCode:
        client = WebClient()
        oauth_v2_response = get_oauth_v2_response(user.slackCode, client)

        if not oauth_v2_response or 'access_token' not in oauth_v2_response:
            logger.debug('slack token received')
            return {'error': 'Problem getting Slack access token. Contact support or try again.'}

    slack_token = oauth_v2_response['access_token']
    authed_user = oauth_v2_response['authed_user']

    user_attr = {
        'email': user.email,
        'username': user.username,
        'hashed_password': get_password_hash(user.password),
        'is_active': False,
    }

    new_user = User(**user_attr)
    db.add(new_user)
    db.commit()

    print('*****', oauth_v2_response)
    if slack_token and client:
        info = get_slack_user_info(slack_token, authed_user['id'], client)

        print('***** info', info)

        slack_profile = {
            'bot_access_token': slack_token,
            'user_access_token': oauth_v2_response.get('authed_user', {}).get('access_token', None),
            'slack_user_id': oauth_v2_response.get('authed_user', {}).get('id', None),
            'team_name': oauth_v2_response.get('team', {}).get('name', None),
            'team_id': oauth_v2_response.get('team', {}).get('id', None),
            'enterprise_name': oauth_v2_response['enterprise']['name'] if oauth_v2_response.get('enterprise') else None,
            'enterprise_id': oauth_v2_response.get['enterprise']['id'] if oauth_v2_response.get('enterprise') else None,
            'email': info.get('profile').get('email', None),
            'first_name': info.get('profile').get('first_name', None),
            'last_name': info.get('profile').get('last_name', None),
            'title': info.get('profile').get('title', None),
            'user_id': new_user.id
        }
        # if they're joining through slack, create the slack user profile
        slack_user_profile = SlackProfile(**slack_profile)
        db.add(slack_user_profile)
        db.commit()
        logger.debug('created slack user profile')
        


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