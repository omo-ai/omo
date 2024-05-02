import logging
from typing import Any
from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserAccountRegistration
from omo_api.settings import AVAILABLE_CONNECTORS, Connector
from omo_api.db.models import (
    User,
    Team,
    PineconeConfig, 
    UserCeleryTasks,
    Account
)
from omo_api.utils import (
    get_env_var, 
    verify_google_jwt, 
    get_current_vector_store,
    get_celery_task_status,
    display_task_status,
    valid_api_token
)

logger = logging.getLogger(__name__) 

router = APIRouter()

def create_user(email: str, db: Session) -> tuple:
    user_attr = {
        'email': email,
    }
    defaults = {
        'username': None,
        'hashed_password': 'NOT_SET',
        'is_active': True
    }

    user, created = get_or_create(db, User, defaults=defaults, **user_attr)

    return user, created

def create_account(user: User, account: UserAccountRegistration, db: Session) -> tuple:
    account_attrs = {
        'type': account.type,
        'provider': account.provider,
        'provider_account_id': account.provider_account_id,
        'refresh_token': account.refresh_token,
        'access_token': account.access_token,
        'expires_at': account.expires_at,
        'id_token': account.id_token,
        'scope': account.scope,
        'session_state': account.session_state,
        'token_type': account.token_type,
        'user_id': user.id
    }

    account, created = get_or_create(db, Account, **account_attrs)

    return account, created

def create_team(user: User, db: Session = Depends(get_db)) -> tuple:
    team_attr = {
        'name': user.email,
        'slug': slugify(user.email),
        'is_active': True
    }
    team, created = get_or_create(db, Team, **team_attr)
    try:
        user.team_id = team.id
        db.add(user)
        db.commit()
    except Exception as e:
        logger.debug(f"could not assign team to user: {e}")
        pass

    return team, created


def create_vecstore_config(user: User, team: Team, db: Session = Depends(get_db)) -> tuple:
    pinecone_kwargs = {
        'index_name': get_env_var('PINECONE_INDEX'),
        'environment': get_env_var('PINECONE_ENV'),
        'api_key': get_env_var('PINECONE_AWS_SECRETS_PATH'),
        'namespaces': [slugify(user.email)],
        'team_id': team.id,
    }

    vecstore_config, created = get_or_create(db, PineconeConfig, **pinecone_kwargs)
    
    return vecstore_config, created

def get_installed_connectors(user: User) -> dict:
    installed_connectors = {
        'connectors': []
    }
    for app in AVAILABLE_CONNECTORS.keys():
        app_configs = getattr(user.team, f"{app}_configs", None)
        # user has existing configs i.e. it's installed
        if not app_configs:
            continue

        installed_connectors['connectors'].append({ 'name': app, 'id': [app_config.id for app_config in app_configs]})

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

    vecstore_config = getattr(user.team, f"{vecstore}_configs")[0]
    for key in keys:
        config['vector_store'][key] = getattr(vecstore_config, key)

    return config

def get_user_team(user: User) -> dict:
    pass

def get_user_files(user_id: int, connector_slug: str, db: Session):

    if connector_slug == Connector.GOOGLE_DRIVE.value:
        user = db.query(User).filter_by(id=user_id).one()
        files = user.team.googledrive_configs[0].files
        return files
    
    return []

############
## Routes ##
############
@router.post('/v2/user/register')
async def register_user(account: UserAccountRegistration,
                        db: Session = Depends(get_db)) -> dict:

    user, user_created = create_user(account.email, db)
    account, account_created = create_account(user, account, db)
    team, team_created = create_team(user, db)
    vecstore_config, vecstore_config_created = create_vecstore_config(user, team, db)
    
    response = {
        "message": "User registered.",
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

@router.get('/v1/user/connectors')
async def get_connector_status(user_id: int, db: Session = Depends(get_db)) -> dict:
    
    query = db.query(UserCeleryTasks)\
            .where(UserCeleryTasks.user_id == user_id)\
            .distinct(UserCeleryTasks.connector)\
            .order_by(UserCeleryTasks.connector, UserCeleryTasks.updated_at.desc())
    
    results = db.execute(query).all() # returns list of tuples

    # shape the response for easy consumption on the frontend
    statuses = []
    for result in results:

        try:
            connector_slug = list(result[0].connector.keys())[0] # e.g googledrive
            display_name = AVAILABLE_CONNECTORS[connector_slug]['display_name']

            celery_task_status = get_celery_task_status(result[0].job_id)['status']
            display_status = display_task_status(celery_task_status)

            files = get_user_files(user_id, connector_slug, db) 

            status = {
                'connector': {
                    'name': display_name,
                    'slug': connector_slug,
                    'ids': list(result[0].connector.values())[0],
                },
                'status': display_status,
                'files': files,
                'files_count': len(files) if files else 0,
            }
            logger.info(status)
            statuses.append(status)
        except Exception as e:
            logger.error(f"Exception fetching user_id {user_id} connectors: {e}")

    return { 'statuses': statuses }