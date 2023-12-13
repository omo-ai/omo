import os
import chromadb
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings, HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough

from dotenv import load_dotenv
from pathlib import Path

#load_dotenv()

ATLASSIAN_USERNAME = '***REMOVED***' #os.getenv('ATLASSIAN_USERNAME')
ATLASSIAN_API_TOKEN = '***REMOVED***' #os.getenv('ATLASSIAN_API_TOKEN')
ATLASSIAN_SPACE_KEY = 'people' # os.getenv('ATLASSIAN_SPACE_KEY')
CHROMADB_HOST = os.getenv('CHROMADB_HOST')
CHROMADB_PORT = os.getenv('CHROMADB_PORT')
CUSTOMER_NS = os.getenv('CUSTOMER_NAMESPACE')
OPENAI_API_KEY = '***REMOVED***' #os.getenv('OPENAI_API_KEY')

#chroma_client = chromadb.HttpClient(host='omo_chromadb_1', port=8000)

loader = ConfluenceLoader(
    url="https://blackarrow.atlassian.net/wiki/",
    username=ATLASSIAN_USERNAME,
    api_key=ATLASSIAN_API_TOKEN
)

documents = loader.load(space_key=ATLASSIAN_SPACE_KEY, include_attachments=True, limit=50)

for document in documents:
    print('document', document)

# # save to disk
# embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# db = Chroma.from_documents(documents, embedding_function, persist_directory="/chroma_index_data")
