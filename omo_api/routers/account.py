import logging
from typing import Any
from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from omo_api.db.utils import get_db, get_or_create
from omo_api.models.user import UserRegister, UserContext
from omo_api.db.models import User, Team, PineconeConfig, UserCeleryTasks
from omo_api.utils import get_env_var
from omo_api.utils.background import get_celery_task_status
from omo_api.utils.vector_store import get_current_vector_store
from omo_api.settings import AVAILABLE_CONNECTORS

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
        user.team_id = team.id
        db.add(user)
        db.commit()
    except Exception as e:
        logger.debug(f"could not assign team to user: {e}")
        pass

    return team


def create_vecstore_config(user: User, team: Team, db: Session = Depends(get_db)):
    pinecone_kwargs = {
        'index_name': get_env_var('PINECONE_INDEX'),
        'environment': get_env_var('PINECONE_ENV'),
        'api_key': get_env_var('PINECONE_AWS_SECRETS_PATH'),
        'namespaces': [slugify(user.email)],
        'team_id': team.id,
    }

    vecstore_config, created = get_or_create(db, PineconeConfig, **pinecone_kwargs)
    
    return vecstore_config

def get_installed_connectors(user: User) -> dict:
    installed_connectors = {
        'connectors': []
    }
    for app in AVAILABLE_CONNECTORS.keys():
        app_configs = getattr(user.team, f"{app}_configs")
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

############
## Routes ##
############

@router.post('/v1/user/register')
async def register_user(user: UserRegister, db: Session = Depends(get_db)) -> dict:
    user_attr = {
        'email': user.email,
    }
    defaults = {
        'username': None,
        'hashed_password': 'NOT_SET',
        'is_active': True
    }

    user, created = get_or_create(db, User, defaults=defaults, **user_attr)
        
    team = create_team(user, db)
    pc_config = create_vecstore_config(user, team, db)

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

@router.get('/v1/user/connectors')
async def get_connector_status(user_id: int, db: Session = Depends(get_db)) -> dict:
    
    query = db.query(UserCeleryTasks)\
            .where(UserCeleryTasks.user_id == user_id)\
            .distinct(UserCeleryTasks.connector)\
            .order_by(UserCeleryTasks.connector, UserCeleryTasks.updated_at.desc())
    
    results = db.execute(query).all() # returns list of tuples

    statuses = []
    for result in results:
        status = {
            'connector': {
                'name': list(result[0].connector.keys())[0],
                'id': list(result[0].connector.values())[0],
            },
            'status': get_celery_task_status(result[0].job_id)['status'],
        }
        print(status)
        statuses.append(status)

    return { 'statuses': statuses }