import json
import logging
from pydantic import BaseModel
from fastapi import Depends, APIRouter, status, HTTPException 
from typing import List, Union
from sqlalchemy import select
from sqlalchemy.orm import Session
from omo_api.db.utils import get_db
from omo_api.db.models.user import User
from omo_api.db.models.googledrive import GDriveObject
from omo_api.models.GoogleDrive import GoogleDriveObject
from omo_api.utils.auth import get_current_active_user

logger = logging.getLogger(__name__) 

router = APIRouter()
@router.get('/v1/confluence/documents')
async def get_confluence_documents(db: Session = Depends(get_db)):
    pass