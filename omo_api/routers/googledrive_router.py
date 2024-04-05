import os
import logging
from fastapi import Depends, APIRouter, Header
from fastapi.encoders import jsonable_encoder
from typing import List, Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.sql import func
from omo_api.models.google_drive import GoogleDriveObjects, GoogleDriveObject
from omo_api.db.utils import get_db
from omo_api.db.models.googledrive import GDriveObject
from omo_api.workers.drive import tasks

from langchain_googledrive.document_loaders import GoogleDriveLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# since environment variable it's a relative to the root of the project, not this file
os.environ['GOOGLE_ACCOUNT_FILE'] = './routers/google_service_key.json'

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v2/googledrive/files')
async def process_gdrive_files(files: GoogleDriveObjects,
                               x_google_authorization: Annotated[str, Header()],
                               db: Session = Depends(get_db)):

    result = tasks.sync_google_drive.delay(jsonable_encoder(files), x_google_authorization)

    return { 'result_id': result.id, 'result_ready': result.ready() }
    