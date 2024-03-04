import os
import sys
from llama_index import download_loader
from omo_api.workers.base import BaseWorker
from omo_api.utils import flatten_list, clean_url
from omo_api.utils.prompt import query_yes_no
from omo_api.loaders.airtable import CustomAirtableReader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

CUSTOMER_KEY='demo'
ENVIRONMENT='development'
ENV_PATH='../../conf/'

load_dotenv(os.path.join(ENV_PATH, f"envs/.env.{ENVIRONMENT}"))
load_dotenv(os.path.join(ENV_PATH, f"envs/{CUSTOMER_KEY}/.env"))



class AirtableWorker(BaseWorker):
    def __init__(self,
                 api_key: str = '',
                 base_id: str = '',
                 table_ids: list = [],
                 format: str = 'langchain'):
        
        self.api_key = api_key
        self.base_id = base_id
        self.table_ids = table_ids
        self.format = format
        self.reader = CustomAirtableReader(api_key=api_key)
        super().__init__()
    
    def load_documents(self):
        all_documents = []
        for tbl_id in self.table_ids:
            documents = self.reader.load_data(table_id=tbl_id, base_id=self.base_id)
            documents = self.format_documents_with_source(documents,
                                                          format=self.format,
                                                          base_id=self.base_id,
                                                          table_id=tbl_id)
            all_documents.append(documents)

        self.documents = flatten_list(all_documents)
        return self.documents

    def format_documents_with_source(self, documents,
                                     format='',
                                     base_id='',
                                     table_id=''):
        
        formatted_docs = []
        for doc in documents:
            if format == 'langchain':
                doc = doc.to_langchain_format()
                doc.metadata['source'] = self.reader.base_metadata[base_id]['tables'][table_id]['url']
                doc.metadata['title'] = self.reader.base_metadata[base_id]['tables'][table_id]['name']

            formatted_docs.append(doc)
        
        return formatted_docs

worker = AirtableWorker(api_key=os.getenv('AIRTABLE_ACCESS_TOKEN'),
                        base_id='appcB965IY5InrQIS',
                        table_ids=['tblpLGCowDETrMhL4', 'tblx58yI3yOx7Jrrp', 'tbl2ZdgQB0k1YKnK0'])

documents = worker.load_documents()
answer = query_yes_no(f"Write {len(documents)} documents to pinecone index: {worker.pinecone_index}?")
if answer:
    worker.to_pinecone(documents)
else:
    print('Exiting...')