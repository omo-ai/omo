import os
import re
import random
import logging
import json
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_openai import OpenAIEmbeddings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.docstore.document import Document
from omo_api.models.chat import Message

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from pinecone.grpc import PineconeGRPC
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

sleep_time = 10/1000 # 10 milliseconds

router = APIRouter()


def preprocess_message(message: str) -> str:
    """
    Strip out strings that make Omo give a weird response
    - hello <@USER_ID2>
    - <@USER_ID2> hello
    """
    try:
        username_pattern = '<@USER_ID2>' # strip out the `OmoAI` username from the message before querying
        message = re.sub(username_pattern, '', message).strip()
    except:
        pass

    return message

def extract_sources(source_documents: List[Document]) -> list:
    """
    Dedupe sources and extra source metadata
    """
    seen_sources = []
    final_sources = []
    for doc in source_documents:
        title = doc.metadata['title']
        source = doc.metadata['source']
        if source not in seen_sources:
            final_sources.append({'title': title, 'source': source}) 
    return final_sources
        

def show_prompt() -> str:
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
         "Looking into it!"
    ]
    prompt_response = random.choice(prompt_responses)
    return f"{prompt_response} Please wait a few moments..."

def sources_from_response(response):
    keys = [
        'file_name',
        'file_path',
        'page_label',
    ]
    source_dict = {
        'sources': [],
    }
    for source in response.source_nodes:
        s = dict.fromkeys(keys, None)

        for k in keys:
            try:
                s[k] = source.metadata[k]
            except:
                pass
        source_dict['sources'].append(s)
    
    return source_dict 

@router.post('/api/v1/chat/')
async def answer_web(message: Message):
    # TODO the context should be provided by the frontend
    return StreamingResponse(answer_question_stream(message.content),
                             media_type="application/json")


import asyncio
async def answer_question_stream(question):
    Settings.llm = OpenAI(model=OPENAI_MODEL)
    Settings.embed_model = OpenAIEmbedding(model=OPENAI_EMBEDDING_MODEL)  

    # These will be customer / context specific
    pc_api_key = os.environ['PINECONE_API_KEY']
    pc_ns = os.environ['PINECONE_NS']
    pc_host = os.getenv('PINECONE_HOST')

    pc = PineconeGRPC(api_key=pc_api_key)
    pinecone_index = pc.Index(host=pc_host)
  
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace=pc_ns)
    index = VectorStoreIndex.from_vector_store(vector_store)
    llm = OpenAI(model=OPENAI_MODEL, temperature=0)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        llm=llm,
        streaming=True)

    response = chat_engine.stream_chat(question)

    for token in response.response_gen:
        answer_chunk = json.dumps( {'answer': token }, ensure_ascii=False) + '\n'
        yield answer_chunk.encode('utf8')
        await asyncio.sleep(sleep_time)
    
    sources_dict = sources_from_response(response)
    sources = json.dumps(sources_dict, ensure_ascii=False) + '\n'
    yield sources.encode('utf8')


def answer_question(question: str, context: dict) -> dict:

    # tmp overrides for ***REMOVED*** 
    #os.environ['PINECONE_API_KEY'] = "***REMOVED***"
    # pinecone_index = "***REMOVED***"
    # pinecone_ns = "***REMOVED***"
    
    os.environ['PINECONE_API_KEY'] = "***REMOVED***"
    os.environ['PINECONE_ENV'] = 'gcp-starter'
    # pinecone_index = context['omo_pinecone_index']
    pinecone_index = 'starter_index'
    pinecone_ns = 'default'
    

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = PineconeVectorStore.from_existing_index(pinecone_index,
                                                        embedding_function,)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

    qa_chain = load_qa_with_sources_chain(llm=llm, chain_type='stuff')

    qa = RetrievalQAWithSourcesChain(
        combine_documents_chain = qa_chain,
        retriever = retriever,
        return_source_documents=True
    )

    answer_response = qa({ 'question': question }, return_only_outputs=False)

    final_answer = {}
    
    if answer_response['sources']:
        sources = extract_sources(answer_response['source_documents'])
    else:
        sources = ''
    
    final_answer['question'] = answer_response['question']
    final_answer['answer'] = answer_response['answer']
    final_answer['sources'] = sources

    return final_answer