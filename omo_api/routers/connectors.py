import logging
from typing import List
from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from omo_api.db.utils import get_db
from omo_api.utils import get_current_active_user
from omo_api.db.models import User, GoogleDriveConfig
from omo_api.config import Connector

logger = logging.getLogger(__name__) 

router = APIRouter()

def get_google_drive_connector(db: Session, user: User, connector_id: str):
    """
    Get details of a Google Drive connector by its ID.

    Args:
        db (Session): The database session.
        user (User): The current active user.
        connector_id (str): The ID of the connector.

    Returns:
        dict: The details of the Google Drive connector.

    Raises:
        HTTPException: If the connector is not found.
    """
    result = db.query(GoogleDriveConfig).filter(GoogleDriveConfig.id == connector_id).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    response = {
        'id': result.id,
        'files': [result.files[key] for key in result.files.keys()],
        'created_at': result.created_at,
        'updated_at': result.updated_at,
        'team_id' : result.team_id,
        'delegate_email': result.delegate_email or "",
    }

    return response 

@router.get('/v1/connectors/{connector_slug}/{connector_id}') 
async def get_connector_by_id(connector_slug: str,
                              connector_id: str,
                              db: Session = Depends(get_db),
                              user: User = Depends(get_current_active_user)):
    """
    Get a connector by its slug and ID.

    Args:
        connector_slug (str): The slug of the connector.
        connector_id (str): The ID of the connector.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The current active user. Defaults to Depends(get_current_active_user).

    Returns:
        dict: The details of the connector.

    Raises:
        HTTPException: If the connector is not found.
    """
    details = None

    if connector_slug == Connector.GOOGLE_DRIVE.value:
        details = get_google_drive_connector(db, user, connector_id)
        # TODO check if the user owns the connector
    
    if not details:
        raise HTTPException(status_code=404, detail="Connector not found")

    return details
