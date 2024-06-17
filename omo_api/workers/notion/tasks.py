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
def sync_notion_pages(self, page_metadata: list, auth_token: str):

    id, title, created_time, last_edited_time, source = page_metadata
    logger.info(f"Starting indexing of Notion page: {id}")

    nw = NotionWorker(token=auth_token)
    documents = nw.load_documents(page_ids=[id])

    updated_docs = []

    logger.debug(documents)
    for doc in documents:
        if doc.id_ == id:
            metadata = {
                'page_id': id,
                'created_time': created_time,
                'last_edited_time': last_edited_time,
                'source': source,
                'title': title,
            }
            doc.metadata = metadata
            updated_docs.append(doc)
        
    # Get the user context
    # Write updated_docs to vector store
