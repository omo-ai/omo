"""
Load data for a POC for Alloy Digital
This script was created because a Google service account was added / shared
directly to a folder
"""
import os
import sys
import logging
from datetime import datetime
import pinecone
import googleapiclient.discovery
from dotenv import load_dotenv 
from typing import Dict, List, Any
from google.oauth2 import service_account
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

from omo_api.db.models import GDriveObject
from omo_api.db.connection import session
from omo_api.utils.prompt import query_yes_no
from omo_api.loaders.gdrive.utils import extract_text, extract_meta_data, load_document_from_file


file_handler = logging.FileHandler(filename='/mnt/efs/tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)

CUSTOMER_KEY='alloydigital'
ENVIRONMENT='production'
ENV_PATH='../../conf/'

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = '/var/www/omo_api/conf/envs/alloydigital/alloydigital.json'
FOLDER_ID = '1VMwza3hvdEU09XCx9XDCxmowudjaTUS9'
DRIVE_CONFIG_ID = 1 # Their GoogleDriveConfig id

load_dotenv(os.path.join(ENV_PATH, f".env.{ENVIRONMENT}"))
load_dotenv(os.path.join(ENV_PATH, f"envs/alloydigital/.env.local"))

#SERVICE_ACCOUNT_FILE = '/var/www/omo_api/routers/google_service_key.json'
#FOLDER_ID = '1pEOAotlJOD4t9epYezpziCEpUF9B2aoi'


### Authenticate with Google API
credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_ACCOUNT_FILE'), scopes=SCOPES)
driveservice = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
docservice =  googleapiclient.discovery.build("docs", "v1", credentials=credentials)

def load_document_from_file(file):
    """Load a GDocs."""
    if file["mimeType"] != "application/vnd.google-apps.document":
        logger.warning(f"File with id '{file['id']}' is not a GDoc")
    else:
        gdoc = docservice.documents().get(documentId=file["id"]).execute()
        text = extract_text(gdoc["body"]["content"])
        return Document(
            page_content="\n".join(text), metadata=extract_meta_data(file)
        )

param = {
    "q": f"'{FOLDER_ID}' in parents and mimeType != 'application/vnd.google-apps.folder'",
    "fields": '*',
}

gdrive_files = driveservice.files()
request = gdrive_files.list(**param)

documents = []
drive_obj_q = []
files_loaded = 0
limit = 20
while request is not None:
    results = request.execute()
    files = results.get('files')

    while files and files_loaded < limit:
        file = files.pop(0)
        logger.debug(f"{files_loaded}: Name: {file['name']}")
        logger.debug(f"   Modified: {file['modifiedTime']}")
        logger.debug(f"   Created: {file['createdTime']}")

        file_id = session.query(GDriveObject).filter(GDriveObject.object_id == file['id']).first()

        if file_id:
            logger.debug(f"File id {file['id']} found. Skipping")
            continue

        link = f"https://docs.google.com/document/d/{file['id']}/edit?usp=drivesdk"
        file["webViewLink"] = link

        doc = load_document_from_file(file)
        
        # Write doc to database
        drive_obj_kwargs = {
            'object_id': doc.metadata['id'],
            'drive_id': DRIVE_CONFIG_ID,
            'service_id': 'docs',
            'name': doc.metadata['name'],
            'description': '',
            'type': 'document',
            'url': doc.metadata['source'],
            'size_bytes': 0,
            'last_edited_at': datetime.fromisoformat(doc.metadata['modifiedTime']),
            'last_synced_at': None,
        }

        drive_obj = GDriveObject(**drive_obj_kwargs) 
        drive_obj_q.append(drive_obj)

        documents.append(doc)

        files_loaded += 1

        logger.debug(f"Num docs: {len(documents)}")

    if files_loaded >= limit:
        break

    request = gdrive_files.list_next(request, results)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_docs = splitter.split_documents(documents)

for (num, doc) in enumerate(split_docs):
    logger.debug(f"{num}: {doc.metadata['name']}...")

index_name = os.getenv('PINECONE_INDEX')

answer = query_yes_no(f"Start loading into index {index_name}. Continue?")

if not answer:
    logger.debug('Exiting.')
    sys.exit()

pinecone.init(
    api_key = os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment = os.getenv("PINECONE_ENV"),  # next to api key in console
)

if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`

embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

logger.debug('Adding to index')

doc_chunk_size = 100

len_split_docs = len(split_docs)
num_iters = len_split_docs / doc_chunk_size
for i in range(0, len_split_docs, doc_chunk_size):
    # loop through so we can track progress
    logger.debug(f"len of split_docs: {len_split_docs}")

    logger.debug(f"On interation {i} of {len_split_docs}...")
    split_docs_chunk = split_docs[i:i + doc_chunk_size]
    docsearch = Pinecone.from_documents(
        split_docs_chunk,
        embedding_function,
        index_name=index_name,
        pool_threads=4, 
        batch_size=64
    )
    logger.debug(f"...loaded chunks {i+doc_chunk_size}")

logger.debug('Finished adding to index')

logger.debug('Committing to DB...')
session.bulk_save_objects(drive_obj_q)
session.commit()
logger.debug('Committed to DB.')