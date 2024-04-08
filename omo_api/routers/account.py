import logging
from typing import Any
from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserRegister
from omo_api.db.models import User, Team, TeamConfig, PineconeConfig
from omo_api.utils import get_env_var
from omo_api.utils.vector_store import *

logger = logging.getLogger(__name__) 

router = APIRouter()


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

def get_installed_connectors(user: User) -> dict:
    installed_connectors = {
        'connectors': []
    }
    for app in AVAILABLE_APPS:
        app_configs = getattr(user.team.team_config, f"{app}_configs")
        # user has existing configs i.e. it's intalled
        if not app_configs:
            continue

        # TODO we probably want to instantiate into response models
        # to control what attributes are sent to the client.
        # get all the columns but delete this key.
        installed_connectors['connectors'][app] = [app_configs.__dict__.pop('_sa_instance_state', None) for app_configs in app_configs]

    return installed_connectors

def get_user_by_email(email: str, db: Session) -> User:
    try:
        user = db.query(User).filter_by(email=email).one()
    except NoResultFound as e:
        logger.debug(f"Exception in get_user: {email} {e}")
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_vector_store_config(user: User) -> dict:
    config = {}
    vecstore = get_current_vector_store()
    keys = ['id', 'index_name', 'environment', 'namespaces', 'created_at', 'updated_at']
    config['vector_store'] = {key: "" for key in keys}
    config['vector_store']['provider'] = vecstore

    vecstore_config = getattr(user.team.team_config, f"{vecstore}_configs")[0]
    for key in keys:
        config['vector_store'][key] = getattr(vecstore_config, key)

    return config

def get_user_team(user: User) -> dict:
    pass

############
## Routes ##
############

@router.post('/v1/user/register')
async def register_user(user: UserRegister, db: Session = Depends(get_db)) -> dict:
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

    response = {
        "message": f"User {user.email} registered.",
        "created": created
    }

    return response

@router.get('/v1/user/', response_model_exclude=['hashed_password', 'username', 'last_login'])
async def get_user(email: str, db: Session = Depends(get_db)) -> dict:
    user = get_user_by_email(email, db)
    user_dict = jsonable_encoder(user)
    installed_apps_dict = get_installed_connectors(user)
    vecstore_config_dict = get_vector_store_config(user)

    response_dict = {}
    response_dict.update(user_dict)
    response_dict.update(installed_apps_dict)
    response_dict.update(vecstore_config_dict)

    return response_dict

    
