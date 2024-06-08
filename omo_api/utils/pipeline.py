import os
import math
import logging
import itertools
from typing import List
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC
from llama_index.core.extractors import TitleExtractor
from llama_index.core.readers.base import BaseReader
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.core.storage.docstore.keyval_docstore import KVDocumentStore
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.core.storage.kvstore.types import BaseKVStore
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.storage.chat_store.redis import RedisChatStore
from llama_index.core.memory import ChatMemoryBuffer
from omo_api.utils import get_env_var, flatten_list

logger = logging.getLogger(__name__)

DEFAULT_BATCH_SIZE = os.environ.get('DEFAULT_BATCH_SIZE', 50)

def get_ingestion_cache() -> RedisCache:
    url = get_env_var('REDIS_URL')
    cache = RedisCache(url)
    logger.info("Instantiated ingestion cache")
    
    return cache


def get_doc_store() -> RedisDocumentStore:

    cache = get_ingestion_cache()
    doc_store = RedisDocumentStore(cache, namespace='llama_index')
    logger.info("Instantiated docstore")

    return doc_store

def get_vector_store(api_key: str, index_name: str, namespace: str) -> BasePydanticVectorStore:
    """Return a Pinecone vector store object"""
    pc = PineconeGRPC(api_key=api_key)
    vector_store = PineconeVectorStore(
        pinecone_index=pc.Index(index_name),
        namespace=namespace,
        batch_size=DEFAULT_BATCH_SIZE
    )

    logger.info("Instatiated vecstore")

    return vector_store

def get_stores(vecstore_index: str, namespace: str):
    vector_store = get_vector_store(api_key=get_env_var('PINECONE_API_KEY'),
                                   index_name=vecstore_index,
                                   namespace=namespace)
    docstore = get_doc_store()
    ingestion_cache = get_ingestion_cache()

    logger.info("Instantiated all stores")

    return vector_store, docstore, ingestion_cache
    
def chunks(iterable, batch_size=DEFAULT_BATCH_SIZE):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

def get_embedding_model():
    llm = get_env_var('LLM').lower()

    if llm == 'openai':
        return OpenAIEmbedding(model=get_env_var('OPENAI_EMBEDDING_MODEL'))

    logger.info(f"got embedding model for LLM {llm}")

    raise NotImplementedError('Embedding model not implemented yet')

def get_chat_model():
    llm = get_env_var('LLM').lower()

    if llm == 'openai':
        return OpenAI(temperature=0.0, model=get_env_var('OPENAI_MODEL'))

    logger.info(f"got chat model for LLM {llm}")
    
    raise NotImplementedError('Chat model not implemented yet')

class SentenceWindowPipeline:
    def __init__(self,
                 docs: list,
                 transforms: list,
                 params: dict,
                #  vector_store: BasePydanticVectorStore,
                 reader: BaseReader = SimpleDirectoryReader,
                 docstore: KVDocumentStore = get_doc_store(),
                 cache: BaseKVStore = get_ingestion_cache()):

        self.docs = docs
        self.transforms = transforms
        self.nodes = None
        self.reader = reader
        self.docstore = docstore
        self.cache = cache

        self.node_parser = SentenceWindowNodeParser.from_defaults(**params)
        self.pipeline = IngestionPipeline(
            transformations=[self.node_parser] + self.transforms,
            docstore=docstore,
            # vector_store=vector_store,
            docstore_strategy=DocstoreStrategy.UPSERTS
        )

    def run(self, num_workers: int = 4):
        try:
            nodes = self.pipeline.run(documents=self.docs, num_workers=num_workers)
            self.nodes = nodes
            return nodes
        except Exception as e:
            logger.error(f"***Exception indexing documents: {e}***")

def get_chat_memory(username: str) -> ChatMemoryBuffer:
    chat_store = RedisChatStore(get_env_var('REDIS_URL'))
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key=username,
    )

    return chat_store, chat_memory
    
def get_pipeline(documents: List[Document], vectore_index: str, namespace: str):

    vecstore, docstore, ingestion_cache = get_stores(vecstore_index=vectore_index,
                                                     namespace=namespace)
    #Settings.text_splitter = SentenceSplitter()

    pipeline = SentenceWindowPipeline(
        docs=flatten_list(documents),
        transforms=[
            # SentenceSplitter(),
            get_embedding_model(),
        ],
        params = {
            # 'sentence_splitter': SentenceSplitter(chunk_size=1024, chunk_overlap=256),
            'window_size': 3,
            'window_metadata_key': 'window',
            'original_text_metadata_key': 'original_text',
        },
        # vector_store=vecstore,
        docstore=docstore,
        cache=ingestion_cache
        
    )
    logger.info(f"got pipeline")
    return pipeline, vecstore, docstore, ingestion_cache

def write_nodes_to_vecstore(nodes, vector_store):
    batches_inserted = 0
    total_batches = math.ceil(len(nodes) / DEFAULT_BATCH_SIZE)
    for chunk in chunks(nodes, batch_size=DEFAULT_BATCH_SIZE):
        try:
            vector_store.add(chunk)
            batches_inserted += 1

            logger.info(f"Added batch {batches_inserted} of {total_batches}")
        except Exception as e:
            logger.error(f"Cannot add chunk: {e}")
            continue

    return batches_inserted, total_batches
