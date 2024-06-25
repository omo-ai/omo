import logging
from sqlalchemy import func, update
from sqlalchemy.sql.functions import coalesce
from omo_api.workers.background import celery
from omo_api.utils.pipeline import get_pipeline, write_nodes_to_vecstore
from omo_api.models.user import UserContext
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.db.models import NotionConfig
from omo_api.loaders.notion import NotionWorker

logger = logging.getLogger(__name__)


@celery.task(bind=True)
def sync_notion_pages(self, user: dict, page_metadata: list, auth_token: str):

    def update_db(page_metadata: list, user_ctx: UserContext):
        page_id, title, created_time, last_edited_time, source = page_metadata
        page_dict = {
            page_id: {
                'title': title,
                'created_time': created_time,
                'last_edited_time': last_edited_time,
                'source': source
            }
        }
        config_kwargs = {
            'team_id': user_ctx.team_id
        }
        logger.info(f"Updating DB with {len(page_dict)} pages")
        # Ensure the NotionConfig object exists
        notion_config, created = get_or_create(session, NotionConfig, **config_kwargs)
        stmt = update(NotionConfig)\
                .where(NotionConfig.team_id == user_ctx.team_id)\
                .values(pages=coalesce(NotionConfig.pages, func.jsonb('{}')) + page_dict)
        result = session.execute(stmt)
        session.commit()

    id, title, created_time, last_edited_time, source = page_metadata
    logger.info(f"Starting indexing of Notion page: {id}")

    nw = NotionWorker(token=auth_token)
    logger.debug('***')
    logger.debug(auth_token)
    documents = nw.load_documents(page_ids=[id])

    updated_docs = []

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

    
    context = UserContext(**user['context'])
        
    index = context.vector_store.index_name
    namespace = context.vector_store.namespaces[0]

    logger.info(f"...writing to index:namespace {index}:{namespace}")

    pipeline, vecstore, docstore, cache = get_pipeline(updated_docs, index, namespace)

    nodes = pipeline.run(num_workers=1)
    num_nodes = len(nodes) if nodes else 0

    logger.debug("...pipelines nodes: %d" % num_nodes)

    if not nodes:
        logger.info("No nodes to write to vecstore")
        return

    batches_inserted, total_batches = write_nodes_to_vecstore(nodes, vecstore)

    if nodes:
        logger.info("updating db...")
        update_db(page_metadata, context)
    
    logger.info(f"...Done indexing Notion for user: {context.email}")

        