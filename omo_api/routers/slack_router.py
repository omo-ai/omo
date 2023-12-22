import os
import pinecone
import logging
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from slack_sdk import WebClient
from fastapi import APIRouter
from omo_api.models.slack import SlackMessagePayload
from typing import Union

logger = logging.getLogger(__name__)

router = APIRouter()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV"), 
)

@router.get('/api/v1/answer_question/{question}')
async def answer_question(question: str):
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(PINECONE_INDEX, embedding_function)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

    rag_prompt = hub.pull("rlm/rag-prompt")
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

    answer = rag_chain.invoke(question)

    logger.debug(f"Question: {question} = Answer: {answer.content}")

    return answer.content


@router.post('/api/v1/slack/receive_message')
async def receive_message(payload: SlackMessagePayload):
    """
    Endpoint that slack will post messages to
    """

    # Slack may send other types to the endpoint 
    if payload.type == 'url_verification' and payload.challenge:
        return payload.challenge

    if payload.event.type == 'message':
        msg = payload.event.text

        answer = await answer_question(msg)

        return answer