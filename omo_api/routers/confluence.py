import logging
from pydantic import BaseModel
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from omo_api.db.utils import get_db
from omo_api.db.models import *

logger = logging.getLogger(__name__) 

router = APIRouter()

class AtlassianConfigModel(BaseModel):
    atlassianApiToken: str
    atlassianUsername: str
    confluenceSpaceKey: str

@router.post('/v1/confluence/config')
async def save_atlassian_config(config: AtlassianConfigModel, db: Session = Depends(get_db)):
    conf = {
        'api_key': config.atlassianApiToken,
        'username': config.atlassianUsername,
    }
    logger.debug(conf)
    new_conf = AtlassianConfig(**conf)
    db.add(new_conf)
    db.commit()

    logger.debug('saved atlassian config')

    space = {
        'space_key': config.confluenceSpaceKey,
        'config_id': new_conf.id
    }
    new_space = ConfluenceSpaceKey(**space)
    db.add(new_space)
    db.commit()

    logger.debug('saved space')

@router.get('/v1/confluence/documents')
async def get_confluence_documents(db: Session = Depends(get_db)):
    pass