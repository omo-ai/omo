import os
import itertools
import pinecone
from pinecone import Pinecone
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
from omo_api.utils import get_env_var, flatten_list

def get_ingestion_cache() -> BaseKVStore:
    host = get_env_var('REDIS_HOST')
    port = get_env_var('REDIS_PORT')

    cache = RedisCache.from_host_and_port(
        host=host, port=port
    )

    return cache


def get_doc_store() -> KVDocumentStore:

    host = get_env_var('REDIS_HOST')
    port = get_env_var('REDIS_PORT')

    doc_store = RedisDocumentStore.from_host_and_port(
        host=host, port=port, namespace='llama_index'
    )

    return doc_store

def get_vector_store(api_key: str, index_name: str, namespace: str) -> BasePydanticVectorStore:
    """Return a Pinecone vector store object"""
    pc = PineconeGRPC(api_key=api_key)
    vector_store = PineconeVectorStore(
        pinecone_index=pc.Index(index_name),
        namespace=namespace
    )

    return vector_store

def get_stores():
    vector_store = get_vector_store(api_key=get_env_var('PINECONE_API_KEY'),
                                   index_name=get_env_var('PINECONE_INDEX'),
                                   namespace=get_env_var('PINECONE_NS'))
    docstore = get_doc_store()
    ingestion_cache = get_ingestion_cache()

    return vector_store, docstore, ingestion_cache
    
def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

class SentenceWindowPipeline:
    def __init__(self,
                 docs: list,
                 transforms: list,
                 params: dict,
                 vector_store: BasePydanticVectorStore,
                 reader: BaseReader = SimpleDirectoryReader,
                 docstore: KVDocumentStore = get_doc_store(),
                 cache: BaseKVStore = get_ingestion_cache()):

        self.docs = docs
        self.transforms = transforms
        self.nodes = None
        self.reader = reader
        self.docstore = docstore
        self.cache = cache

        self.node_parser = SentenceWindowNodeParser(**params)
        self.pipeline = IngestionPipeline(
            transformations=[self.node_parser] + self.transforms,
            docstore=docstore,
            vector_store=vector_store,
            docstore_strategy=DocstoreStrategy.UPSERTS
        )

    def run(self, num_workers: int = 4):
        nodes = self.pipeline.run(documents=self.docs, num_workers=num_workers)
        self.nodes = nodes

        return self.nodes
    
def get_pipeline(documents: List[Document]):
    vecstore, docstore, ingestion_cache = get_stores()
    pipeline = SentenceWindowPipeline(
        docs=flatten_list(documents),
        transforms=[
            SentenceSplitter(),
            Settings.embed_model,
        ],
        params = {
            'window_size': 3,
            'window_metadata_key': 'window',
            'original_text_metadata_key': 'original_text',
        },
        vector_store=vecstore,
        docstore=docstore,
        cache=ingestion_cache
        
    )
    return pipeline