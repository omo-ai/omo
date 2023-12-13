import os
import pinecone
from langchain_googledrive.document_loaders import GoogleDriveLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone


#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials/google/credentials.json'
os.environ['GOOGLE_ACCOUNT_FILE'] = '../routers/google_service_key_2.json'
os.environ["PINECONE_API_KEY"] = '37a5136a-01b3-42d2-b90c-c448f66452eb'
os.environ["PINECONE_ENV"] = 'gcp-starter'
os.environ["OPENAI_API_KEY"] = '***REMOVED***' #os.getenv('OPENAI_API_KEY')

index_name = 'alloydigital-demo'

# loader = GoogleDriveLoader(
#     folder_id="1rkTUQegW5L87cB9_vNDDVYrYX3CTlwNM",
#     recursive=True
# )

loader = GoogleDriveLoader(
    file_ids = ["1o1llsOTIGloSRxfgxoArHHrhTxZGdBqd-ya4PtglWec"],
)

documents = loader.load()
print(documents)

# pinecone.init(
#     api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
#     environment=os.getenv("PINECONE_ENV"),  # next to api key in console
# )

# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`


# print(f'Found {len(documents)} documents...')

# for doc in documents:
#     print("---")
#     print(doc.page_content.strip()[:60] + "...")


# embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# docsearch = Pinecone.from_documents(documents, embedding_function, index_name=index_name)