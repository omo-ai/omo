import os
import re
import pinecone
import random
import logging
import json
from typing import List
from queue import Queue
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain import hub
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from omo_api.models.web import WebMessagePayload
from omo_api.routers.callbacks import QueueCallbackHandler

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')



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


@router.post('/api/v1/web/answer/')
async def answer_web(payload: WebMessagePayload):
    # TODO the context should be provided by the frontend
    return StreamingResponse(answer_question_stream(payload.question),
                             media_type="application/json")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel

async def answer_question_stream(question):
    pc_api_key = os.environ['PINECONE_API_KEY']
    pc_env = os.environ['PINECONE_ENV']
    pc_index = os.environ['PINECONE_INDEX']

    pinecone.init(
        api_key=pc_api_key, 
        environment=pc_env
    )

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(pc_index, embedding_function)
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
        yield json.dumps({'answer': chunk.get('answer')})

        if 'context' in chunk:
            yield json.dumps(
                {'sources': [doc.metadata['source'] for doc in chunk['context'] ]}
            )


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

    pinecone.init(
        api_key=context['omo_pinecone_api_key'], 
        environment=context['omo_pinecone_env'], 
    )

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(context['omo_pinecone_index'], embedding_function)
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