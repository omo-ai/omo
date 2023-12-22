import os
import pinecone
import json
import logging
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from slack_sdk import WebClient
from fastapi import APIRouter, Request
from omo_api.models.slack import SlackMessagePayload
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV"), 
)

bolt_app = AsyncApp()
bolt_app_handler = AsyncSlackRequestHandler(bolt_app)

router = APIRouter()

@router.post("/api/v1/slack/message")
async def endpoint(req: Request):
    return await bolt_app_handler.handle(req)

@bolt_app.event("message")
async def handle_message(body, say, logger):
    # prompt_responses = [
    #     "Getting the answer for you!",
    #     "I'm on it!",
    #     "Good question! Let me see."
    # ]

    # question = message['text']
    # prompt_response = random.choice(prompt_responses)
    # say(f"{prompt_response} Please wait a few moments...")
    # response = requests.get(f'http://{API_HOST}/api/v1/answer_question/{question}')

    logger.debug(f"Challenge body: {body}")
    # say(response.text)
    payload = json.loads(body)
    say(payload['challenge'])



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




# @router.post('/api/v1/slack/receive_message')
# async def receive_message(payload: SlackMessagePayload):
#     """
#     Endpoint that slack will post messages to
#     """

#     # Slack may send other types to the endpoint 
#     if payload.type == 'url_verification' and payload.challenge:
#         return payload.challenge

#     if payload.event.type == 'message':
#         msg = payload.event.text

#         answer = await answer_question(msg)

#         return answer