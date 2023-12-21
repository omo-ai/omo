"""
Load data for a POC for Alloy Digital
This script was created because a Google service account was added / shared
directly to a folder
"""
import os
import re
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

logger = logging.getLogger(__name__)

CUSTOMER_KEY='alloydigital'
ENVIRONMENT='development'
ENV_PATH='../../conf/'

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = '/var/www/omo_api/conf/envs/alloydigital/alloydigital.json'
FOLDER_ID = '1VMwza3hvdEU09XCx9XDCxmowudjaTUS9'
DRIVE_CONFIG_ID = 1 # Their GoogleDriveConfig id

load_dotenv(os.path.join(ENV_PATH, f".env.{ENVIRONMENT}"))
load_dotenv(os.path.join(ENV_PATH, f"envs/.env.{CUSTOMER_KEY}"))

#SERVICE_ACCOUNT_FILE = '/var/www/omo_api/routers/google_service_key.json'
#FOLDER_ID = '1pEOAotlJOD4t9epYezpziCEpUF9B2aoi'


def extract_text(
        node: Any,
        *,
        key: str = "content",
        path: str = "/textRun",
        markdown: bool = True,
    ) -> List[str]:
        def visitor(result: List[str], node: Any, parent: str) -> List[str]:
            return_link = False # defaults to false in original code
            if isinstance(node, dict):
                if "paragraphMarker" in node:
                    result.append("- " if "bullet" in node["paragraphMarker"] else "")
                    return result
                if "paragraph" in node:
                    prefix = ""
                    named_style_type = node["paragraph"]["paragraphStyle"][
                        "namedStyleType"
                    ]
                    level = re.match("HEADING_([1-9])", named_style_type)
                    if level:
                        prefix = f"{'#' * int(level[1])} "
                    if "bullet" in node["paragraph"]:
                        prefix += "- "
                    result.append(prefix)
                if "table" in node:
                    col_size = [0 for _ in range(node["table"]["columns"])]
                    rows: List[List[Any]] = [[] for _ in range(node["table"]["rows"])]
                    for row_idx, row in enumerate(node["table"]["tableRows"]):
                        for col_idx, cell in enumerate(row["tableCells"]):
                            body = "".join(
                                visitor([], cell, parent + "/table/tableCells/[]")
                            )
                            # remove URL to calculate the col max size
                            pure_body = re.sub(r"\[(.*)\](?:\(.*\))", r"\1", body)
                            cell_size = max(3, len(max(pure_body.split("\n"), key=len)))
                            col_size[col_idx] = max(col_size[col_idx], cell_size)
                            str_cell = re.sub(r"\n", r"<br />", "".join(body).strip())
                            rows[row_idx].append(str_cell)
                    # Reformate to markdown with extra space

                    for row in rows:
                        for col_idx, cell in enumerate(row):
                            split_cell = re.split(r"(<br />|\n)", cell)
                            # Split each portion and pad with space
                            for i, portion in enumerate(split_cell):
                                if portion != "<br />":
                                    pure_portion = re.sub(
                                        r"\[(.*)\](?:\(.*\))", r"\1", portion
                                    )
                                    split_cell[i] = portion + (
                                        " " * (col_size[col_idx] - len(pure_portion))
                                    )
                            # rebuild the body
                            row[col_idx] = "".join(split_cell)
                    # Now, build a markdown array
                    for row_idx, row in enumerate(rows):
                        row_result = ["| "]
                        for cell in row:
                            row_result.append(f"{cell} | ")
                        result.append("".join(row_result) + "\n")
                        if row_idx == 0:
                            row_result = ["|"]
                            for col_idx in range(len(row)):
                                row_result.append(("-" * (col_size[col_idx] + 2)) + "|")
                            result.append("".join(row_result) + "\n")
                    return result

                if key in node and isinstance(node.get(key), str):
                    if parent.endswith(path):
                        if node[key].strip():
                            if markdown and (
                                ("style" in node and "link" in node["style"])
                                or ("textStyle" in node and "link" in node["textStyle"])
                            ):
                                style_node = (
                                    node["style"]
                                    if "style" in node
                                    else node["textStyle"]
                                )
                                link = style_node["link"]
                                if isinstance(link, dict):
                                    link = link.get("url")
                                if return_link and link:
                                    result[-1] = f"{result[-1]}[{node[key]}]({link})"
                                else:
                                    # Empty link
                                    result[-1] = f"{result[-1]}{node[key]}"
                            else:
                                result[-1] = f"{result[-1]}{node[key]}"

                for k, v in node.items():
                    visitor(result, v, parent + "/" + k)
            elif isinstance(node, list):
                for v in node:
                    visitor(result, v, parent + "/[]")
            return result

        result: List[str] = []
        visitor(result, node, "")
        # Clean the result:
        purge_result = []
        previous_empty = False
        for line in result:
            line = re.sub("\x0b\s*", "\n", line).strip()
            if not line:
                if previous_empty:
                    continue
                previous_empty = True
            else:
                previous_empty = False

            purge_result.append(line)
        return purge_result

def extract_meta_data(file: Dict) -> Dict:
    """
    Extract metadata from file

    :param file: The file
    :return: Dict the meta data
    """
    meta = {
        "gdriveId": file["id"],
        "id": file["id"],
        "mimeType": file["mimeType"],
        "name": file["name"],
        "title": file["name"],
    }
    if file["webViewLink"]:
        meta["source"] = file["webViewLink"]
    else:
        logger.debug(f"Invalid URL {file}")
    if "createdTime" in file:
        meta["createdTime"] = file["createdTime"]
    if "modifiedTime" in file:
        meta["modifiedTime"] = file["modifiedTime"]
    if "sha256Checksum" in file:
        meta["sha256Checksum"] = file["sha256Checksum"]
    if "owners" in file:
        meta["author"] = file["owners"][0]["displayName"]
    if file.get("description", "").strip():
        meta["summary"] = file["description"]
    return meta

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

credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_ACCOUNT_FILE'), scopes=SCOPES)
driveservice = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
docservice =  googleapiclient.discovery.build("docs", "v1", credentials=credentials)

param = {
    "q": f"'{FOLDER_ID}' in parents and mimeType != 'application/vnd.google-apps.folder'",
    "fields": '*',
}
# result = driveservice.files().list(**param).execute()
# files = result.get('files')

gdrive_files = driveservice.files()
request = gdrive_files.list(**param)

documents = []
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
        files_loaded += 1


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

        session.add(drive_obj)
        session.commit()

        logger.debug(f"Commited objected: {doc.metadata['name']}")

        documents.append(doc)

        logger.debug(f"Num docs: {len(documents)}")

    if files_loaded >= limit:
        break

    request = gdrive_files.list_next(request, results)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
split_docs = splitter.split_documents(documents)



for (index, doc) in enumerate(split_docs):
    logger.debug(f"{index}: {doc.metadata['name']}...")

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
docsearch = Pinecone.from_documents(split_docs, embedding_function, index_name=index_name)

logger.debug('Finished adding to index')

folder_kwargs ={
    'service_id': 'docs',
    'name': 'Tactiq Transcripts',
    'description': '',
    'type': 'folder', # document
    'last_edited_utc': 0,
    'url': '',
    'size_bytes': 0,
    'drive_id': 1,
}