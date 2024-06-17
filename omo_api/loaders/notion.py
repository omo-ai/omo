import os
import sys
import logging
from typing import Optional, Union
from llama_index.readers.notion import NotionPageReader
from omo_api.workers.base import BaseWorker
from omo_api.utils import flatten_list, clean_url
from omo_api.utils.prompt import query_yes_no

logger = logging.getLogger(__name__)

"""
Uses llama-index document readers. As of this writing, langchain
can only load databases, not pages. llama-index can handle both.
"""
class NotionWorker(BaseWorker):
    def __init__(self,
                 token: str = '',
                 base_url: Union[str, None] = None,
                 doc_format: Union[str, None] = None):

        super().__init__()
        self.token = token
        self.documents = []
        self.doc_format = doc_format

        self.reader = NotionPageReader(integration_token=token)

    
    def load_documents(self, page_ids: list = None, db_ids: list = None):
        all_documents = []

        if page_ids:
            logger.debug(f"Loading {len(page_ids)} Notion pages...")
            documents = self.load_pages(page_ids=page_ids)
            all_documents.append(documents)
        
        if db_ids:
            documents = self.load_databases(database_ids=db_ids)
            all_documents.append(documents)

        documents = flatten_list(all_documents)

        self.documents = documents
        # self.add_source_metadata()
        self.doc_format_documents()

        return self.documents

    def load_databases(self, database_ids: list): 
        db_docs = []
        for db_id in database_ids:
            documents = self.reader.load_data(database_id=db_id)
            db_docs.append(documents)

        return flatten_list(db_docs)
     
    def load_pages(self, page_ids: list):
        documents = self.reader.load_data(page_ids=page_ids)
        return documents

    def doc_format_documents(self):
        if self.doc_format == 'langchain':
            self.documents = [doc.to_langchain_doc_format() for doc in self.documents]
        

