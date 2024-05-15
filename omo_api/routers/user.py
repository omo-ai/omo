import json
import uuid
import logging
import redis
from typing import Any, Optional
from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserAccountRegistration
from omo_api.db.models.chat import Chat
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
    get_current_vector_store,
    get_celery_task_status,
    display_task_status,
    get_current_active_user,
    get_cache_client,
    valid_api_token,
)

logger = logging.getLogger(__name__) 

router = APIRouter()

ENV = get_env_var('ENV')

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

# def get_user_by_email(email: str, db: Session) -> User:
#     try:
#         user = db.query(User).filter_by(email=email).one()
#     except NoResultFound as e:
#         logger.debug(f"Exception in get_user: {email} {e}")
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

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

def get_chat_by_user_id(db: Session, user_id: str) -> Optional[Chat]:
    result = db.query(Chat).filter(Chat.user_id == user_id).one_or_none()
    return result

############
## Routes ##
############
from fastapi import Cookie, Request, Response, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Union
http_bearer = HTTPBearer(auto_error=True)

from fastapi_nextauth_jwt import NextAuthJWT

JWT = NextAuthJWT(
    secret=get_env_var("AUTH_SECRET"),
)
@router.get('/v1/whoami')
async def me (user: Annotated[User, Depends(get_current_active_user)]):
    return { 'email': user.email }


@router.get('/v1/me', response_model_exclude=['hashed_password', 'username', 'last_login'])
async def get_user(user: Annotated[User, Depends(get_current_active_user)]) -> dict:
    
    user_dict = jsonable_encoder(user)
    installed_apps_dict = get_installed_connectors(user)
    vecstore_config_dict = get_vector_store_config(user)

    response_dict = {}
    response_dict.update(user_dict)
    response_dict.update(installed_apps_dict)
    response_dict.update(vecstore_config_dict)

    return response_dict


@router.post('/v2/users/register')
async def register_user(account: UserAccountRegistration,
                        response: Response,
                        db: Session = Depends(get_db)) -> dict:

    user, user_created = create_user(account.email, db)
    account, account_created = create_account(user, account, db)
    team, team_created = create_team(user, db)
    vecstore_config, vecstore_config_created = create_vecstore_config(user, team, db)

    response = {
        "message": "User registered.",
    } 
    return response

@router.get('/v1/users/inflight/{registration_id}')
async def get_registration_in_flight(registration_id: str, 
                                     depends=Depends(valid_api_token)):
    client = get_cache_client()
    result = client.get(registration_id)

    if not result:
        raise HTTPException(status_code=404, detail="Registration not found")

    account_info = json.loads(result)

    return {'message': 'Registration found', 'data': account_info}

@router.post('/v1/users/inflight')
async def create_registration_in_flight(response: Response,
                                        account: UserAccountRegistration,
                                        depends=Depends(valid_api_token)):
    
    # client.hset('omo:registrations_in_flight', mapping={'b5635b11-8f22-4bbc-af1e-6d520b200560': "{'email': 1}"})
    cache = get_cache_client()

    key_namespace = "omo:registrations_in_flight"
    uuid_key = str(uuid.uuid4())

    account_as_string = json.dumps(jsonable_encoder(account))
    cache.hset(key_namespace, mapping={uuid_key: account_as_string})

    secure = True if ENV == 'prod' else False
    response.set_cookie(key='omo.registration_id', value=uuid_key, 
                        secure=secure, samesite='Lax')
    
    return { 'message': f"Registration: {uuid_key}"}

@router.get('/v1/users/connectors')
async def get_connector_status(user: Annotated[dict, Depends(get_current_active_user)],
                               db: Session = Depends(get_db)) -> dict:
    
    query = db.query(UserCeleryTasks)\
            .where(UserCeleryTasks.user_id == user.id)\
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

            files = get_user_files(user.id, connector_slug, db) 

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
            logger.error(f"Exception fetching user_id {user.id} connectors: {e}")

    return { 'statuses': statuses }


@router.get("/v1/users/{user_id}/chats/")
async def get_chat_for_user(user_id: str, db: Session = Depends(get_db)):
    try:
        chat = get_chat_by_user_id(db, user_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail="Multiple chats found for this user")