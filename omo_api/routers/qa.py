import os
import re
import pinecone
import random
import logging
from operator import itemgetter
from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter
from langchain import hub
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from omo_api.conf.prompt import PROMPT_TEMPLATE
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')



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


def answer_question(question: str, context: dict) -> dict:

    pinecone.init(
        api_key=context['omo_pinecone_api_key'], 
        environment=context['omo_pinecone_env'], 
    )

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(context['omo_pinecone_index'], embedding_function)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

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