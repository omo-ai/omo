import os
import logging
from sqlalchemy import update, insert
from sqlalchemy.orm import Session
from fastapi import APIRouter, Header, Depends
from fastapi.encoders import jsonable_encoder
from typing import List, Annotated
from omo_api.models.google_drive import GoogleDriveObject
from omo_api.models.user import UserContext
from omo_api.workers.drive import tasks
from omo_api.db.models.user import UserCeleryTasks
from omo_api.db.utils import get_db
from omo_api.settings import Connector

# since environment variable it's a relative to the root of the project, not this file
os.environ['GOOGLE_ACCOUNT_FILE'] = './routers/google_service_key.json'

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v2/googledrive/files')
async def process_gdrive_files(files: List[GoogleDriveObject],
                               user_context: UserContext,
                               x_google_authorization: Annotated[str, Header()],
                               db: Session = Depends(get_db)):

    logger.debug('Submitting celery job')

    task_result = tasks.sync_google_drive.delay(
        jsonable_encoder(files),
        jsonable_encoder(user_context),
        x_google_authorization
    )

    try:
        # TODO we need to get the connectors from server side
        # client can tamper with any of the payload
        connector_ids = None
        for connector in user_context.connectors:
            if connector.name == Connector.GOOGLE_DRIVE.value:
                connector_ids = connector.id

        logger.debug(f"Inserting into celery job table: {task_result.id}")
        stmt = insert(UserCeleryTasks)\
                .values(
                    user_id=user_context.id,
                    job_id=task_result.id,
                    connector={Connector.GOOGLE_DRIVE.value: connector_ids}
                )
        result = db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.error(f"Could not save celery task ID {task_result.id} to db: {e}")

    return { 'result_id': task_result.id, 'result_ready': task_result.ready() }
    