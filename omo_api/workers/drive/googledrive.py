import os
import sys
import pinecone
from dotenv import load_dotenv 
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from omo_api.loaders import CustomGoogleDriveLoader
from omo_api.utils.prompt import query_yes_no

CUSTOMER_KEY='komodo'
ENVIRONMENT='development'

ENV_PATH='../../conf/'

# file_ids = [
#     '1o1llsOTIGloSRxfgxoArHHrhTxZGdBqd-ya4PtglWec', # anyone with the link (GD Onboarding); folder
#     '1YkPhX3V1B3neXITJ9Zue-STgAnzQ2iX067_b4qBp3Vk', # copy of above, root folder, anyone with link
#     '1yP1a109PaQGRLhRUiud0C2cfpb-r5VInvhg2ZPcL3D0', # anyone within the group, (Doc shared within org), root folder
#     '1fphmphVQRf50KR7K2nEAXea2c680sOzdCxZObKNeX5Q', # public (GD Service Accounts), root folder
# ]
folder_ids = [
    '1pEOAotlJOD4t9epYezpziCEpUF9B2aoi'
]

document_ids = []

######## END CONFIGURATION. DO NOT MODIFY BELOW LINE #########

load_dotenv(os.path.join(ENV_PATH, f".env.{ENVIRONMENT}"))
load_dotenv(os.path.join(ENV_PATH, f"envs/.env.{CUSTOMER_KEY}"))

for folder in folder_ids:
    print(f"Folder: {folder}")

for doc in document_ids:
    print(f"File: {doc}")

answer = query_yes_no(f"Manually loading for {CUSTOMER_KEY}. Continue?")

if not answer:
    print('Exiting.')
    sys.exit()


all_docs = []

if folder_ids:
    for folder_id in folder_ids:
        loader = CustomGoogleDriveLoader(
            folder_id=folder_id,
            recursive=True
        )
        folder_documents = loader.load()

        if len(folder_documents) > 0:
            print(f"Found {len(folder_documents)} documents in folder.")
            all_docs.extend(folder_documents)

if document_ids:
    loader = CustomGoogleDriveLoader(
        document_ids=document_ids,
    )
    documents = loader.load()
    if len(documents) > 0:
        all_docs.extend(documents)

for (index, doc) in enumerate(all_docs):
    print(f"{index}: {doc.metadata['name']}...")

index_name = os.getenv('PINECONE_INDEX')

answer = query_yes_no(f"Start loading into index {index_name}. Continue?")

if not answer:
    print('Exiting.')
    sys.exit()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)
index_name = os.getenv('PINECONE_INDEX')
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`

embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
docsearch = Pinecone.from_documents(all_docs, embedding_function, index_name=index_name)