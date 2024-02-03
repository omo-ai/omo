import os
import pinecone

class BaseWorker:
    def __init__(self,
                 pinecone_index=None,
                 pinecone_env=None,
                 pinecone_key=None):

        self.pinecone_index = pinecone_index or os.getenv('PINECONE_INDEX', None)
        self.pinecone_env = pinecone_env or os.getenv('PINECONE_ENV', None)
        self.pinecone_key = pinecone_key or os.getenv('PINECONE_KEY', None)

        pinecone.init(
            api_key=self.pinecone_key,
            environment=self.pinecone_env,
        )