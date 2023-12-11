import logging
from fastapi import Depends, APIRouter
from typing import List, Union
from sqlalchemy.orm import Session
from models.GoogleDrive import GoogleDriveObjects
from db.utils import get_db
from db.models.googledrive import GDriveObject

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v1/googledrive/files')
async def save_file(files: GoogleDriveObjects,
                    db: Session = Depends(get_db) ):

    for file in files.files:
        
        file_info = {
            'gdrive_id': file.id,
            'service_id': file.serviceId,
            'name': file.name,
            'description': file.description,
            'type': file.type,
            'last_edited_utc': file.lastEditedUtc,
            'url': file.url,
            'size_bytes': file.sizeBytes
        }

        logger.debug('adding new file...', file_info)

        new_file = GDriveObject(**file_info)
        db.add(new_file)
        db.commit()

        logger.debug('...successfully added file')