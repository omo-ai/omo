import os
import sys
from llama_index import download_loader
from omo_api.workers.base import BaseWorker
from omo_api.utils import flatten_list, clean_url
from omo_api.utils.prompt import query_yes_no
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

"""

"""
class AirtableWorker(BaseWorker):
    def __init__(self,
                 api_key: str = '',
                 base_id: str = '',
                 table_id: str = '',
                 format: str = 'langchain'):
        
        self.api_key = api_key
        self.base_id = base_id
        self.table_id = table_id
        self.format = format

        AirtableReader = download_loader('AirtableReader')
        self.reader = AirtableReader(api_key)
    
    def load_documents(self):
        documents = self.reader.load_data(table_id=self.table_id, base_id=self.base_id)
        self.documents = documents

        self.format_documents()

        return self.documents

    def format_documents(self):
        if self.format == 'langchain':
            self.documents = [doc.to_langchain_format() for doc in self.documents]

worker = AirtableWorker(api_key=os.getenv('AIRTABLE_ACCESS_TOKEN'),
                        base_id='appcB965IY5InrQIS',
                        table_id='tblpLGCowDETrMhL4')

documents = worker.load_documents()
print(documents)
