import os
import re
import random
import logging
import json
import asyncio
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from pinecone.grpc import PineconeGRPC
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import Settings
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.vector_stores.pinecone import PineconeVectorStore
# from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
# from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain.docstore.document import Document
from omo_api.db.models import User, Chat
from omo_api.models.chat import Message
from omo_api.utils.pipeline import (
    get_chat_model, 
    get_embedding_model,
    get_vector_store,
    get_chat_memory
)
from omo_api.db.utils import get_or_create
from omo_api.db.connection import session
from omo_api.utils import get_current_active_user
from omo_api.models.user import UserContext
from sqlalchemy import update, func
from sqlalchemy.sql.functions import coalesce


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

# def extract_sources(source_documents: List[Document]) -> list:
#     """ Dedupe sources and extra source metadata for the Slack response
#     """
#     seen_sources = []
#     final_sources = []
#     for doc in source_documents:
#         title = doc.metadata['title']
#         source = doc.metadata['source']
#         if source not in seen_sources:
#             final_sources.append({'title': title, 'source': source}) 
#     return final_sources
        

def show_prompt() -> str:
    """Display the initial response message in the Slack response
    """
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
         "Looking into it!"
    ]
    prompt_response = random.choice(prompt_responses)
    return f"{prompt_response} Please wait a few moments..."

def append_to_chat_history(chat_id: str, user: User, question_dict: dict, answer_dict: dict):
    """Append the question and answer to the chat's history
    """
    chat_kwargs = {
        'user_id': user.id,
        'chat_id': chat_id,
    }

    combined_messages =  jsonable_encoder([question_dict, answer_dict]),
    
    chat, created = get_or_create(session, Chat, **chat_kwargs)

     # TODO this will only work with latin languages. Need to handle other languages
     # it won't work if the title is in Chinese, for example
    max_words = 6
    if created:
        title = question_dict['content']
        split_title = title.split()
        if len(split_title) >= max_words:
            suffix = '...'
        else:
            suffix = ''

        chat.title = ' '.join(split_title[:max_words]) + suffix

    # two separates queries to keep the messages flat; don't append a list of dicts
    # i.e. [{ question_dict }, { answer_dict}, ...]
    stmt = update(Chat)\
            .where(Chat.chat_id == chat_id, Chat.user_id == user.id)\
            .values(messages=coalesce(Chat.messages, func.jsonb('{}')) + combined_messages)
    result = session.execute(stmt)
    session.commit()



def sources_from_response(response) -> list:
    """Dedupe and return a source documents

    :param response: The response from the ChatEngine
    :return: list of dictionaries
    :rtrype: list
    """

    """
    The structure of the sources dict:
    sources = {
        '/path/to/file.pdf': {
            'file_name': 'file.pdf',
            'file_path': '/path/to/file.pdf',
            'page_labels': [12, 34],
            'creation_date': timestamp,
            'last_modified_date': timestamp,
        }
    }
    """
    sources = {}
    for source in response.source_nodes:
        file_path = source.metadata.get('file_path', None)

        if not file_path:
            file_path = source.metadata.get('source', None)
        
        if not file_path:
            continue

        file_name = source.metadata.get('file_name', None)
        mimetype = source.metadata.get('mimetype', None)
        creation_date = source.metadata.get('creation_date', None)
        last_modified_date = source.metadata.get('last_modified_date', None)

        page_label = source.metadata.get('page_label', None)
        page = source.metadata.get('page', None)

        if file_path not in sources.keys():
            sources[file_path] = {}            
            sources[file_path]['page_labels'] = []

        sources[file_path]['file_name'] = file_name or file_path
        sources[file_path]['file_path'] = file_path
        sources[file_path]['mimetype'] = mimetype
        sources[file_path]['creation_date'] = creation_date 
        sources[file_path]['last_modified_date'] = last_modified_date 

        if page_label and page_label not in sources[file_path]['page_labels']:
            sources[file_path]['page_labels'].append(page_label)
        
        if page and page not in sources[file_path]['page_labels']:
            sources[file_path]['page_labels'].append(page)

    """
    Transform dict to list to make it easier for frontend to parse
    [{
        'file_name': 'file.pdf',
        'file_path': '/path/to/file.pdf',
        'page_labels': [12, 34],
    }, ...]
    """
    sources_list = [sources[key] for key in sources.keys()]

    return sources_list

@router.post('/v1/chat/', tags=["question_and_answering"])
async def answer_web(message: Message,
                     user: User = Depends(get_current_active_user)):
    """
    Answer a user question or prompt and stream the response
    """

    return StreamingResponse(answer_question_stream(message, user),
                             media_type="application/json")


async def answer_question_stream(message: Message, user: User):

    # these will be used to append to the chat's history
    question_dict = {
        'role': 'human',
        'content': message.content
    }

    answer_dict = {
        'role': 'assistant',
        'content': '',
        'sources': [],
    }

    question = message.content
    chat_id = message.chat_id

    llm = get_chat_model()
    # no other way to locally use the embedding model
    Settings.embed_model = get_embedding_model()
    
    # TODO make this vector store agnostic
    pc_api_key = os.environ['PINECONE_API_KEY']

    vector_store = get_vector_store(
        pc_api_key,
        user.context['vector_store']['index_name'],
        user.context['vector_store']['namespaces'][0],
    )

    index = VectorStoreIndex.from_vector_store(vector_store)

    chat_store, chat_memory = get_chat_memory(username=user.email)

    # default 3000 token memory
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        llm=llm,
        streaming=True,
        memory=chat_memory,
        similarity_top_k=2,
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window")
    ],  )

    response = chat_engine.stream_chat(question)

    for token in response.response_gen:
        answer_dict['content'] += token
        answer_chunk = json.dumps( {'answer': token }, ensure_ascii=False) + '\n'
        yield answer_chunk.encode('utf8')
        await asyncio.sleep(sleep_time)
    
    sources_list = sources_from_response(response)
    sources = json.dumps({ 'sources': sources_list }, ensure_ascii=False) + '\n'
    answer_dict['sources'] = sources_list
    yield sources.encode('utf8')

    # append the question and answer to the chat's history
    append_to_chat_history(chat_id, user, question_dict, answer_dict)