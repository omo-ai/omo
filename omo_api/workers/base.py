import os
import logging
import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

logger = logging.getLogger(__name__)

class BaseWorker:
    def __init__(self,
                 pinecone_index=None,
                 pinecone_env=None,
                 pinecone_key=None,
                 openai_key=None):

        self.pinecone_index = pinecone_index or os.getenv('PINECONE_INDEX', None)
        self.pinecone_env = pinecone_env or os.getenv('PINECONE_ENV', None)
        self.pinecone_key = pinecone_key or os.getenv('PINECONE_KEY', None)
        self.openai_key = openai_key or os.getenv('OPENAI_API_KEY', None)
        self.documents = None

        pinecone.init(
            api_key=self.pinecone_key,
            environment=self.pinecone_env,
        )
    
    def to_pinecone(self, documents):
        """
        Write documents to Pinecone
        """
        if not documents:
            logger.debug('BaseWorker.to_pinecone: Nothing to write.')
            return False

        try:
            embedding_function = OpenAIEmbeddings(openai_api_key=self.openai_key)
            docsearch = Pinecone.from_documents(documents, embedding_function, index_name=self.pinecone_index)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            raise

        return True
