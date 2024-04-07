import os
import logging
from fastapi import APIRouter, Header
from fastapi.encoders import jsonable_encoder
from typing import List, Annotated
from omo_api.models.google_drive import GoogleDriveObject
from omo_api.models.user import UserContext
from omo_api.workers.drive import tasks

# since environment variable it's a relative to the root of the project, not this file
os.environ['GOOGLE_ACCOUNT_FILE'] = './routers/google_service_key.json'

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v2/googledrive/files')
async def process_gdrive_files(files: List[GoogleDriveObject],
                               user_context: UserContext,
                               x_google_authorization: Annotated[str, Header()]):

    result = tasks.sync_google_drive.delay(
        jsonable_encoder(files),
        jsonable_encoder(user_context),
        x_google_authorization
    )

    return { 'result_id': result.id, 'result_ready': result.ready() }
    