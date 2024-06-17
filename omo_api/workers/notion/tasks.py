import json
import math
import logging
import requests
from omo_api.workers.background import celery
from omo_api.utils.pipeline import get_pipeline, chunks, write_nodes_to_vecstore, DEFAULT_BATCH_SIZE
from omo_api.models.user import UserContext
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.utils.background import TaskStates
from omo_api.utils import flatten_list
from omo_api.loaders.notion import NotionWorker

logger = logging.getLogger(__name__)

@celery.task(bind=True)
def sync_notion_pages(self, page_id: str, auth_token: str):
    logger.info(f"Starting indexing of Notion page: {page_id}")

    nw = NotionWorker(token=auth_token)
    documents = nw.load_documents(page_ids=[page_id])
    logger.debug(documents)
