import os
import logging
from datetime import timedelta
from typing import Annotated, Optional, Union
from fastapi import Depends, APIRouter, status, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserRegister, Token
from omo_api.db.models import User, Team, TeamConfig, PineconeConfig
from omo_api.utils import get_env_var
from slugify import slugify

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v1/user/register')
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    user_attr = {
        'email': user.email,
        'username': None,
        'hashed_password': 'NOT_SET',
        'is_active': True
    }

    user, created = get_or_create(db, User, **user_attr)
    
    team = create_team(user, db)
    team_config = create_teamconfig(team, db)
    pc_config = create_vecstore_config(user, team_config, db)

    response_msg = f"User {user.email} registered. Created: {created}"

    return response_msg

def create_team(user: User, db: Session = Depends(get_db)):
    team_attr = {
        'name': user.email,
        'slug': slugify(user.email),
        'is_active': True
    }
    team, created = get_or_create(db, Team, **team_attr)
    try:
        user.team_id = team.team_id
        db.add(user)
        db.commit()
    except Exception as e:
        logger.debug(f"could not assign team to user: {e}")
        pass

    return team

def create_teamconfig(team: Team, db: Session = Depends(get_db)):
    teamconfig_attrs = {
        'team_id': team.id
    }
    teamconfig, created = get_or_create(db, TeamConfig, **teamconfig_attrs)
    return teamconfig

def create_vecstore_config(user: User, team_config: TeamConfig, db: Session = Depends(get_db)):
    pinecone_kwargs = {
        'index_name': get_env_var('PINECONE_INDEX'),
        'environment': get_env_var('PINECONE_ENV'),
        'api_key': get_env_var('PINECONE_API_KEY_PATH'),
        'namespaces': [slugify(user.email)],
        'team_config_id': team_config.id,
    }

    vecstore_config, created = get_or_create(db, PineconeConfig, **pinecone_kwargs)
    
    return vecstore_config