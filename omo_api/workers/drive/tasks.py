import json
import math
import billiard as multiprocessing
from sqlalchemy import update, select, func
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.dialects.postgresql import JSONB
from celery.utils.log import get_task_logger
from omo_api.loaders.gdrive.google_drive import GoogleDriveReaderOAuthAccessToken
from omo_api.workers.background import celery
from omo_api.utils.pipeline import get_pipeline, chunks, write_nodes_to_vecstore, DEFAULT_BATCH_SIZE
from omo_api.models.user import UserContext
from omo_api.db.models.googledrive import GoogleDriveConfig
from omo_api.db.connection import session
from omo_api.db.utils import get_or_create
from omo_api.utils.background import TaskStates
from omo_api.utils import flatten_list

logger = get_task_logger(__name__) 

@celery.task(bind=True)
def sync_google_drive(self, file: dict, user: dict, access_token: str):

    def update_db(file: dict, user_ctx: UserContext):
        # files_dict = {f['id']: f for f in files}
        files_dict = { file['id']: file }
        config_kwargs = {
            'team_id': user_ctx.team_id
        }
        logger.info(f"Updating DB with {len(files_dict)} files")
        # Ensure the GoogleDriveConfig object exists
        gdrive_config, created = get_or_create(session, GoogleDriveConfig, **config_kwargs)
        stmt = update(GoogleDriveConfig)\
                .where(GoogleDriveConfig.team_id == user_ctx.team_id)\
                .values(files=coalesce(GoogleDriveConfig.files, func.jsonb('{}')) + files_dict) # append files
        result = session.execute(stmt)
        session.commit()

    logger.debug('Starting sync_google_drive task')

    # self.update_state(task_id=self.request.id, state=TaskStates.PROGRESS.value)

    loader = GoogleDriveReaderOAuthAccessToken(access_token=access_token)
    context = UserContext(**user['context'])

    logger.info(f"indexing for user: {context.email}...")

    all_docs = []
    file_type = file['type']

    # Anything > 1 leads to 
    # AssertionError: daemonic processes are not allowed to have children
    num_workers = 1

    if file_type == 'folder':
        folder_docs = loader.load_data(
            folder_id=file['id'],
            num_workers=num_workers,
        )
        all_docs.append(folder_docs)
    elif file_type in ('file', 'document'):
        docs = loader.load_data(
            file_ids=[file['id']],
            num_workers=num_workers,
        )
        all_docs.append(docs)
    else:
        logger.error(f"Invalid file type: {file['type']}")
        return

    logger.debug(f"...num all_docs: {len(all_docs)}")

    if not all_docs:
        logger.info('...all_docs empty')
        return
    
    # get the vector store info based on User (fetch from server side)
    # pass into get pipeline and init pinecone
    # note namespaces are created automatically if it doesn't exist
    index = context.vector_store.index_name
    namespace = context.vector_store.namespaces[0] # currently user only has one namespace
    logger.info(f"...writing to index:namespace {index}:{namespace}")

    documents = flatten_list(all_docs)

    pipeline, vecstore, docstore, cache = get_pipeline(documents, index, namespace)

    # anything > 1 daemonic processes are not allowed to have children
    # seems to be becauase celery uses a custom implementatio of multiprocessing
    # called billiard, and llama-index uses the standard multiprocessing
    nodes = pipeline.run(num_workers=1)

    num_nodes = len(nodes) if nodes else 0

    logger.debug("...pipelines nodes: %d" % num_nodes)

    if not nodes:
        logger.info('...no nodes. exiting')
        return

    batches_inserted, total_batches = write_nodes_to_vecstore(nodes, vecstore)

    if nodes:
        # only write the files to db if we could successfully add to vec store
        logger.info("updating db...")
        update_db(file, context)

    logger.info(f"...Done indexing for user: {context.email}")
    