import os
import re
import random
import logging
import json
import asyncio
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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
from omo_api.models.chat import Message
from omo_api.utils.pipeline import get_chat_model, get_embedding_model, get_vector_store
from omo_api.models.user import UserContext


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


def sources_from_response(response):
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

@router.post('/v1/chat/')
async def answer_web(message: Message):
    # TODO the context should be provided by the frontend
    return StreamingResponse(answer_question_stream(message.content,
                                                    message.user_context),
                             media_type="application/json")


async def answer_question_stream(question: str, user_context: UserContext):

    llm = get_chat_model()
    # no other way to locally use the embedding model
    Settings.embed_model = get_embedding_model()
    
    # TODO make this vector store agnostic
    pc_api_key = os.environ['PINECONE_API_KEY']

    vector_store = get_vector_store(
        pc_api_key,
        user_context.vector_store.index_name,
        user_context.vector_store.namespaces[0])

    index = VectorStoreIndex.from_vector_store(vector_store)

    # default 3000 token memory
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        llm=llm,
        streaming=True,
        similarity_top_k=2,
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window")
    ],  )

    response = chat_engine.stream_chat(question)

    for token in response.response_gen:
        answer_chunk = json.dumps( {'answer': token }, ensure_ascii=False) + '\n'
        yield answer_chunk.encode('utf8')
        await asyncio.sleep(sleep_time)
    
    sources_dict = sources_from_response(response)
    sources = json.dumps({ 'sources': sources_dict }, ensure_ascii=False) + '\n'
    yield sources.encode('utf8')


# def answer_question(question: str, context: dict) -> dict:

#     # tmp overrides for ***REMOVED*** 
#     #os.environ['PINECONE_API_KEY'] = "***REMOVED***"
#     # pinecone_index = "***REMOVED***"
#     # pinecone_ns = "***REMOVED***"
    
#     os.environ['PINECONE_API_KEY'] = "***REMOVED***"
#     os.environ['PINECONE_ENV'] = 'gcp-starter'
#     # pinecone_index = context['omo_pinecone_index']
#     pinecone_index = 'starter_index'
#     pinecone_ns = 'default'
    

#     embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
#     docsearch = PineconeVectorStore.from_existing_index(pinecone_index,
#                                                         embedding_function,)
#     retriever = docsearch.as_retriever()

#     llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

#     qa_chain = load_qa_with_sources_chain(llm=llm, chain_type='stuff')

#     qa = RetrievalQAWithSourcesChain(
#         combine_documents_chain = qa_chain,
#         retriever = retriever,
#         return_source_documents=True
#     )

#     answer_response = qa({ 'question': question }, return_only_outputs=False)

#     final_answer = {}
    
#     if answer_response['sources']:
#         sources = extract_sources(answer_response['source_documents'])
#     else:
#         sources = ''
    
#     final_answer['question'] = answer_response['question']
#     final_answer['answer'] = answer_response['answer']
#     final_answer['sources'] = sources

#     return final_answer