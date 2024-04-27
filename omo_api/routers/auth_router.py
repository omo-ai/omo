import os
import logging
from datetime import timedelta
from typing import Annotated, Optional
from fastapi import Depends, APIRouter, status, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserRegister, Token
from omo_api.db.models import User, SlackProfile
from omo_api.utils.auth import get_password_hash, authenticate_user, create_access_token
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
from slack_sdk.errors import SlackApiError

ACCESS_TOKEN_EXPIRE_MINUTES = 60*60*24

logger = logging.getLogger(__name__) 

router = APIRouter()

SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')

def get_oauth_v2_access(temp_auth_code: str,
                          client: WebClient) -> Optional[SlackResponse]:
    """
    Get an OAuth access code from a temporary code
    """
    try:
        response = client.oauth_v2_access(
            client_id=SLACK_CLIENT_ID,
            client_secret=SLACK_CLIENT_SECRET,
            code=temp_auth_code,
        )
        return response

    except SlackApiError as e:
        logger.debug(f"slack api error: {e}")
        return None

def get_slack_user_info(token: str, slack_user_id: str,
                        client: WebClient) -> Optional[SlackResponse]:
    """
    Retrieve Slack profile info to enrich context
    """
    try:
        info = client.users_profile_get(token=token, user=slack_user_id)
        return info
    except SlackApiError as e: 
        logger.debug(f"slack api error: {e}")
        return None

def create_slack_profile(db: Session,
                         slack_token: str,
                         oauth_v2_response: SlackResponse,
                         info: SlackResponse,
                         user_obj: User) -> Union[SlackProfile, bool]:
    # if they're joining through slack, create the slack user profile
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
        'user_id': user_obj.id
    }

    with db.begin():
        slack_user_profile = SlackProfile(**slack_profile)
        db.add(slack_user_profile)
        db.commit()
        logger.debug('created slack user profile')

    return slack_user_profile or False

@router.post('/v1/user/register')
async def register_user(user: UserRegister, db: Session = Depends(get_db)):

    user_attr = {
        'email': user.email,
        'username': None,
        'hashed_password': 'NOT_SET',
    }

    user_obj, created = get_or_create(db, User, **user_attr)
    response_msg = f"User {user_obj.email} registered. Created: {created}"

    if user.slackCode:
        # The slackCode is provided from the frontend. The value is provided
        # during the flow where the user installs the slack app.
        # get the Oauth access token for the slack user
        client = WebClient()
        oauth_v2_response = get_oauth_v2_access(user.slackCode, client)

        if not oauth_v2_response or 'access_token' not in oauth_v2_response:
            logger.debug('slack token received')
            return {'error': 'Problem getting Slack access token. Contact support or try again.'}

        slack_token = oauth_v2_response['access_token']
        authed_user = oauth_v2_response['authed_user']

        info = get_slack_user_info(slack_token, authed_user['id'], client)
        slack_profile = create_slack_profile(db, slack_token, oauth_v2_response, info, user_obj)
        if slack_profile:
            response_msg += f" Created Slack Profile: {slack_profile.id}"
            logger.debug(response_msg)
        else:
            logger.debug(f"Could not create Slack Profile.")

    return response_msg

@router.post('/v1/user/login', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
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

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email, 
    }