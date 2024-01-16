import os
import sys
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import ConfluenceLoader
from langchain.vectorstores import Pinecone
from omo_api.utils.prompt import query_yes_no
import pinecone

from dotenv import load_dotenv

CUSTOMER_KEY='demo'
ENVIRONMENT='production'

ENV_PATH='../../conf/'

load_dotenv(os.path.join(ENV_PATH, f"envs/.env.{ENVIRONMENT}"))
load_dotenv(os.path.join(ENV_PATH, f"envs/{CUSTOMER_KEY}/.env"))

for name, value in os.environ.items():
    print("{0}: {1}".format(name, value))

def get_space_keys():
    keys = os.getenv('CONFLUENCE_SPACE_KEYS')
    space_keys = keys.split(',')

    return space_keys


spaces = get_space_keys()

if not spaces:
    print('No spaces set in CONFLUENCE_SPACE_KEYS. Exiting.')
    sys.exit()

answer = query_yes_no(f"Manually loading for {CUSTOMER_KEY}. Continue?")

if not answer:
    print('Exiting')
    sys.exit()


loader = ConfluenceLoader(
    #url=os.getenv('CONFLUENCE_BASE_URL'),
    url='https://blackarrow.atlassian.net/wiki',
    username=os.getenv('ATLASSIAN_USERNAME'),
    api_key=os.getenv('ATLASSIAN_API_TOKEN')
)

all_docs = []
for space in spaces:
    print(f"Loading documents for space {space}")
    # `space_key`, `page_ids`, `label`, `cql` parameters
    documents = loader.load(
        space_key=space,
        include_attachments=True,
        limit=50
    )
    all_docs.extend(documents)


for (index, document) in enumerate(all_docs):
    print(f"{index}: {document.metadata['title']}")

answer = query_yes_no(f"Found {len(all_docs)} documents. Continue?")
if not answer:
    print('Exiting.')
    sys.exit()

index_name = os.getenv('PINECONE_INDEX')
print(f"Writing to index {index_name}...")

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)

embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
docsearch = Pinecone.from_documents(all_docs, embedding_function, index_name=index_name)
print(f"...Done")
