import os
import sys
from llama_index import download_loader
from omo_api.workers.base import BaseWorker
from omo_api.utils import flatten_list, clean_url
from omo_api.utils.prompt import query_yes_no
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

"""
Uses llama-index document loaders. As of this writing, langchain
can only load databases, not pages. llama-index can handle both.
"""
class NotionWorker(BaseWorker):
    def __init__(self,
                 integration_token: str = '',
                 base_url: str ='',
                 format: str ='langchain'):

        super().__init__()
        self.integration_token = integration_token
        self.base_url = clean_url(base_url)
        self.documents = []
        self.format = format

        NotionPageReader = download_loader('NotionPageReader')
        self.reader = NotionPageReader(integration_token=integration_token)

    
    def load_documents(self, page_ids: list = None, db_ids: list = None):
        all_documents = []

        if page_ids:
            documents = self.load_pages(page_ids=page_ids)
            all_documents.append(documents)
        
        if db_ids:
            documents = self.load_databases(database_ids=db_ids)
            all_documents.append(documents)

        documents = flatten_list(all_documents)

        self.documents = documents
        self.add_source_metadata()
        self.format_documents()

        return self.documents

    def load_databases(self, database_ids: list): 
        db_docs = []
        for db_id in database_ids:
            documents = self.reader.load_data(database_id=db_id)
            db_docs.append(documents)

        return flatten_list(db_docs)
    
    def get_source_url(self, page_or_db_id: str):
        cleaned_id = page_or_db_id.replace('-', '') 
        return f"{self.base_url}/{cleaned_id}"

    def add_source_metadata(self):
        for doc in self.documents:
            source_url = self.get_source_url(doc.metadata['page_id'])
            doc.metadata['source'] = source_url
            doc.metadata['title'] = source_url
        
            
    def load_pages(self, page_ids: list):
        documents = self.reader.load_data(page_ids=page_ids)
        return documents

    def format_documents(self):
        if self.format == 'langchain':
            self.documents = [doc.to_langchain_format() for doc in self.documents]
        

if __name__ == '__main__':
    page_ids = [
        '7ab5d27093a647cbafedc0241e0d2d39', # Parent Product page
    ]
        
    notion_worker = NotionWorker(
        integration_token=os.getenv('NOTION_API_TOKEN'),
        base_url='https://notion.so/blackarrowai'
    )
    documents = notion_worker.load_documents(page_ids=page_ids)
    print(documents)

    answer = query_yes_no(f"Manually loading {len(documents)} Notion document. Continue?")

    if not answer:
        sys.exit()

    index_name = notion_worker.pinecone_index
    print(f"Writing to index {index_name}...")

    embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    docsearch = Pinecone.from_documents(documents, embedding_function, index_name=index_name)
    print(f"...Done")

