import os
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from omo_api.loaders import CustomGoogleDriveLoader

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/var/www/omo_api/routers/google_service_key.json'
os.environ['GOOGLE_ACCOUNT_FILE'] = '/var/www/omo_api/routers/google_service_key.json'
os.environ['GOOGLE_DELEGATE_EMAIL'] = 'omo-service@helloomo.ai'
os.environ["PINECONE_API_KEY"] = '37a5136a-01b3-42d2-b90c-c448f66452eb'
os.environ["PINECONE_ENV"] = 'gcp-starter'
os.environ["OPENAI_API_KEY"] = '***REMOVED***' #os.getenv('OPENAI_API_KEY')

index_name = 'alloydigital-demo'

# Document level permissions are not inherited from folder
file_ids = [
    '1o1llsOTIGloSRxfgxoArHHrhTxZGdBqd-ya4PtglWec', # anyone with the link (GD Onboarding); folder
    '1YkPhX3V1B3neXITJ9Zue-STgAnzQ2iX067_b4qBp3Vk', # copy of above, root folder, anyone with link
    '1yP1a109PaQGRLhRUiud0C2cfpb-r5VInvhg2ZPcL3D0', # anyone within the group, (Doc shared within org), root folder
    '1fphmphVQRf50KR7K2nEAXea2c680sOzdCxZObKNeX5Q', # public (GD Service Accounts), root folder
]

# loader = GoogleDriveLoader(
#     folder_id="1rkTUQegW5L87cB9_vNDDVYrYX3CTlwNM",
#     recursive=True
# )

loader = CustomGoogleDriveLoader(
    document_ids=file_ids,
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