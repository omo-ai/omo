import json
from sqlalchemy import update, select, func
from celery.utils.log import get_task_logger
from omo_api.loaders.gdrive.google_drive import GoogleDriveReaderOAuthAccessToken
from omo_api.workers.background import celery
from omo_api.utils.pipeline import get_pipeline
from omo_api.models.user import UserContext
from omo_api.db.models.googledrive import GoogleDriveConfig
from omo_api.db.connection import session

logger = get_task_logger(__name__) 

@celery.task
def sync_google_drive(files: dict, user_context: dict, access_token: str):

    def update_db(files: dict, user_ctx: UserContext):
        files_dict = {f['id']: f for f in files}
        stmt = update(GoogleDriveConfig)\
                .where(GoogleDriveConfig.team_id == user_ctx.team_id)\
                .values(files=GoogleDriveConfig.files + files_dict) # append files
        result = session.execute(stmt)
        session.commit()

    loader = GoogleDriveReaderOAuthAccessToken(access_token=access_token)
    context = UserContext(**user_context)

    logger.info(f"indexing for user: {context.email}...")

    folders = filter(lambda f: f['type'] == 'folder', files)
    files = list(filter(lambda f: f['type'] != 'folder', files))

    folder_ids = [f['id'] for f in folders]
    file_ids = [f['id'] for f in files]

    all_docs = []
    for folder_id in folder_ids:
        folder_docs = loader.load_data(folder_id=folder_id)
        all_docs.append(folder_docs)

    logger.info(f"...total number of docs: {len(all_docs)}")
    docs = loader.load_data(file_ids=file_ids)
    all_docs.append(docs)

    # get the vector store info based on User (fetch from server side)
    # pass into get pipeline and init pinecone
    index = context.vector_store.index_name
    namespace = context.vector_store.namespaces[0] # currently user only has one namespace
    logger.info(f"...writing to index:namespace {index}:{namespace}")
    # note namespaces are created automatically if it doesn't exist
    pipeline = get_pipeline(all_docs, index, namespace)
    nodes = pipeline.run(num_workers=1) # anything > 1 results in AttributeError: Can't pickle local object 'split_by_sentence_tokenizer.<locals>.split'
    logger.debug(nodes)
    logger.info(f"...Done indexing for user: {context.email}")

    logger.info("updating db...")
    update_db(files, context)



        
            