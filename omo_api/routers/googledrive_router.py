import os
import logging
import pinecone
from fastapi import Depends, APIRouter, Header
from typing import List, Union, Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.sql import func
from omo_api.models.google_drive import GoogleDriveObjects, GoogleDriveObject
from omo_api.db.utils import get_db
from omo_api.db.models.googledrive import GDriveObject
from omo_api.workers.drive import tasks
from omo_api.loaders.gdrive.google_drive import GoogleDriveReaderOAuthAccessToken
from omo_api.utils import flatten_list
from omo_api.utils.pipeline import (
    SentenceWindowPipeline,
    get_stores,
)

from langchain_googledrive.document_loaders import GoogleDriveLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.extractors import TitleExtractor
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.readers.google import GoogleDriveReader
from llama_index.llms.openai import OpenAI

# since environment variable it's a relative to the root of the project, not this file
os.environ['GOOGLE_ACCOUNT_FILE'] = './routers/google_service_key.json'

logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post('/v2/googledrive/files')
async def process_gdrive_files(files: GoogleDriveObjects,
                               x_google_authorization: Annotated[str, Header()],
                               db: Session = Depends(get_db)):
    
    loader = GoogleDriveReaderOAuthAccessToken(access_token=x_google_authorization)

    folders = filter(lambda f: f.type == 'folder', files.files)
    files = filter(lambda f: f.type != 'folder', files.files)

    folder_ids = [f.id for f in folders]
    file_ids = [f.id for f in files]

    all_docs = []
    for folder_id in folder_ids:
        folder_docs = loader.load_data(folder_id=folder_id)
        all_docs.append(folder_docs)

    docs = loader.load_data(file_ids=file_ids)
    all_docs.append(docs)

    vecstore, docstore, ingestion_cache = get_stores()

    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    Settings.llm = OpenAI(temperature=0.0, model="gpt-4-0125-preview")

    pipeline = SentenceWindowPipeline(
        docs=flatten_list(all_docs),
        transforms=[
            SentenceSplitter(),
            Settings.embed_model,
        ],
        params = {
            'window_size': 3,
            'window_metadata_key': 'window',
            'original_text_metadata_key': 'original_text',
        },
        vector_store=vecstore,
        docstore=docstore,
        cache=ingestion_cache
        
    )
    nodes = pipeline.run(num_workers=1) # anything > 1 results in AttributeError: Can't pickle local object 'split_by_sentence_tokenizer.<locals>.split'
    logger.debug(nodes)
    

@router.post('/v1/googledrive/files')
async def save_file(files: GoogleDriveObjects,
                    db: Session = Depends(get_db) ):

    logger.debug('ALL FILES', files)
    process_files_q = []
    upsert_files_q = []
    skip_files = []
    for file in files.files:
        
        stmt = select(
            GDriveObject.id,
            GDriveObject.gdrive_id,
            GDriveObject.size_bytes,
            GDriveObject.last_edited_utc,
            GDriveObject.last_synced_at,
            GDriveObject.type,
        ).filter(GDriveObject.gdrive_id == file.id)

        try:
            result = db.execute(stmt)
            drive_object = result.one_or_none()
        except MultipleResultsFound as e:
            msg = {'error': 'Multiple gdrive IDs found.'}
            logger.debug("multiple Ids found. Cannot reconcile.")
            return msg

        if drive_object:
            logger.debug('got drive object')
            # check if file has been modified
            # if so, update and reprocess
            if drive_object.last_edited_utc == file.lastEditedUtc and drive_object.last_synced_at:
                logger.debug('file has not been modified and already processed. skipping.')
                skip_files.append(file)
                continue
            else:
                # found in the database, but has been edited or not init'ed
                logger.debug('found in database and attempting again...')
                upsert_files_q.append(drive_object)

        else:
            logger.debug('no existing drive object found. adding to q.')
            process_files_q.append(file)

    if len(process_files_q) > 0 or len(upsert_files_q) > 0:
        logger.debug('queues not empty. processing.')
        process_files(db, process_files_q, upsert_files_q)
    else:
        logger.debug('both qs empty. noop.')
    
def process_files(db: Session, files: List[GoogleDriveObject], upsert_files: List[GoogleDriveObject]):

    logger.debug('Processing New Files', files)
    logger.debug('Processing Existing Files', upsert_files)

    folder_ids = []
    file_ids = []
    
    for file in files:
        file_info = {
            'gdrive_id': file.id,
            'service_id': file.serviceId,
            'name': file.name,
            'description': file.description,
            'type': file.type,
            'last_edited_utc': file.lastEditedUtc,
            'url': file.url,
            'size_bytes': file.sizeBytes,
            'last_synced_at': None,
        }

        logger.debug('adding new file to db...', file_info)

        new_file = GDriveObject(**file_info)
        db.add(new_file)
        db.commit()

        if file.type == 'folder':
            folder_ids.append(new_file)
        if file.type == 'document':
            file_ids.append(new_file)

    # This files were attempted previously, but failed to import
    for existing_file in upsert_files:
        if existing_file.type == 'folder':
            folder_ids.append(existing_file)
        if existing_file.type == 'document':
            file_ids.append(existing_file)

    logger.debug('starting embedding process...')

    embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    index_name = os.getenv('PINECONE_INDEX') # TODO exit if index name not found

    logger.debug(f"...got index name {index_name}")
    logger.debug(f"...found {len(folder_ids)} folders")
    logger.debug(f"...found {len(file_ids)} files")

    error_folder = 0
    error_file = 0

    # create vector embeddings
    # TODO process documents asynchronously
    if file_ids:
        for file in file_ids:
            try:
                """
                We loop through file_ids and create embeddings for each individual document.
                Batch processing using the GoogleDriveLoader.file_ids parameter is all or none
                If one file fails, it all fails. With this approach, if one file fails, it continues
                """
                logger.debug(f"trying file id {file.id}")
                logger.debug(f"gdrive id {file.gdrive_id}")
                file_loader = GoogleDriveLoader(
                    file_ids = [file.gdrive_id], 
                )
                documents = file_loader.load()
                docsearch = Pinecone.from_documents(documents, embedding_function, index_name=index_name)
                logger.debug(f"...added {file.gdrive_id} file_ids to {index_name}") 
                file.last_synced_at = func.now() 
                db.add(file)
                db.commit()
            except Exception as e:
                error_file += 1
                logger.debug(f"** error processing id: {file.id} gdrive_id: {file.gdrive_id}: {e}")
                continue

        
    for folder in folder_ids:
        # langchain does not support batch loading multiple folders
        try:
            folder_loader = GoogleDriveLoader(
                folder_id=folder.gdrive_id,
                recursive = True,
            )
            folder_documents = folder_loader.load()
            docsearh_folder = Pinecone.from_documents(folder_documents, embedding_function, index_name=index_name) 
            logger.debug(f"...added {folder.gdrive_id} folder_ids to {index_name}" )
            folder.last_synced_at = func.now() 

            db.add(folder)
            db.commit()
        except Exception as e:
            error_folder += 1
            logger.debug(f"** failed to process id: {folder.id} gdrive_id: {folder.gdrive_id}: {e}")
            continue

    total_errors = error_folder + error_file
    if error_folder + error_file > 0:
        msg = {"message": f"{total_errors} files or folders failed to sync."}
    else:
        msg = {"message": f"All files synced successfully."}

    return msg
    