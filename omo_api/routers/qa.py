import os
import re
import pinecone
import random
import logging
import json
import time
from typing import List
from queue import Queue
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain import hub
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_openai import OpenAIEmbeddings
#from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from omo_api.models.chat import Message

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

sleep_time = 10/1000 # 10 milliseconds

router = APIRouter()

# @router.post('/api/v1/user/prompt')
# async def ask(prompt: str):

#     def generator(prompt: str):
#         for item in llm.stream(prompt):
#             yield item

#     return StreamingResponse(
#         generator(question.prompt), media_type='text/event-stream')

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


# @router.post('/api/v1/chat/')
# async def answer(payload: MessageHistoryPayload):
#     # TODO the context should be provided by the frontend
#     messages = payload.messages
#     message = messages[-1] # gets the most recent message
#     return StreamingResponse(answer_question_stream(message.content),
#                              media_type="application/json")

@router.post('/api/v1/chat/')
async def answer_web(message: Message):
    # TODO the context should be provided by the frontend
    return StreamingResponse(answer_question_stream(message.content),
                             media_type="application/json")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



async def answer_question_stream(question):
    pc_api_key = os.environ['PINECONE_API_KEY']
    pc_env = os.environ['PINECONE_ENV']
    pc_index = os.environ['PINECONE_INDEX']
    pc_ns = os.environ['PINECONE_NS']

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                                          model=OPENAI_EMBEDDING_MODEL)
    docsearch = PineconeVectorStore.from_existing_index(pc_index,
                                                        embedding_function,
                                                        namespace=pc_ns)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name=OPENAI_MODEL,
                    temperature=0,
                    openai_api_key=OPENAI_API_KEY)
                    # callbacks=[QueueCallbackHandler(Queue())],
                    #callbacks=[QueueCallbackHandler(queue=Queue())],
                    # streaming=True,
                    # verbose=True)

    prompt = hub.pull("rlm/rag-prompt")
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    for chunk in rag_chain_with_source.stream(question):
        answer = chunk.get('answer') 
        answer_chunk = json.dumps({'answer': answer}, ensure_ascii=False).encode('utf8')
        yield answer_chunk + b'\n'
        time.sleep(sleep_time) # the server produces chunks faster than the client can consume them.

        if 'context' in chunk:
            source_chunk = json.dumps(
                {'sources': [doc.metadata['source'] for doc in chunk['context'] ]},
                ensure_ascii=False
            ).encode('utf8')
            yield source_chunk + b'\n' #jsonlines
            time.sleep(sleep_time)

    

    # qa = RetrievalQAWithSourcesChain.from_chain_type(
    #     chain_type='stuff',
    #     llm=llm,
    #     retriever = retriever
    # )
    # yield qa(question)['answer'] # we can shift parsing of the source results to the frontend


    # qa_chain = load_qa_with_sources_chain(llm=llm, chain_type='stuff')

    # qa = RetrievalQAWithSourcesChain(
    #     combine_documents_chain = qa_chain,
    #     retriever = retriever,
    #     return_source_documents=True
    # )

    #yield qa({ 'question': question }, return_only_outputs=False)
    # print(qa({ 'question': question }, return_only_outputs=False))
    # yield qa(question)


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