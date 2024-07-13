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
from omo_api.config import Connector


logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v2/googledrive/files', tags=["google_drive"])
async def index_google_drive_files(
        files: List[GoogleDriveObject],
        user_context: UserContext,
        x_google_authorization: Annotated[str, Header(
            description="Google access token. Obtained by the client \
            performing the OAuth flow with Google."
        )],
        db: Session = Depends(get_db)) -> dict:

    """
    Indexes Google Drive files by passing them to Celery for processing
    """
    logger.debug('Submitting celery job')

    chunk_size = 2
    task_result = tasks.sync_google_drive.chunks(
        [
            (jsonable_encoder(file), jsonable_encoder(user_context), x_google_authorization,)
            for file in files
        ],
        chunk_size
    ).apply_async()
    logger.debug(f"group_id: {task_result.id}")
    # write the Task Set ID (aka GroupResult) to the backend (Redis) so we can
    # retrieve it and the child IDs and their status later
    task_result.save() 

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
                    job_id=f"group_id:{task_result.id}",
                    connector={Connector.GOOGLE_DRIVE.value: connector_ids}
                )
        result = db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.error(f"Could not save celery task ID {task_result.id} to db: {e}")

    return { 'result_id': task_result.id, 'result_ready': task_result.ready() }
    