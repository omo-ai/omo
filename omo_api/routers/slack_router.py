import os
import re
import pinecone
import random
import logging
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from fastapi import APIRouter, Request
from omo_api.models.slack import SlackMessagePayload
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

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

# These need to align with the Slack events we're receiving
oauth_required_scopes = [
    "channels:read",
    "groups:read",
    "chat:write",
    "app_mentions:read",
    "reactions:read"
]

oauth_settings = OAuthSettings(
    client_id=SLACK_CLIENT_ID,
    client_secret=SLACK_CLIENT_SECRET,
    scopes=oauth_required_scopes,
    installation_store=FileInstallationStore(base_dir="/mnt/efs/slack/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="/mnt/efs/slack/states")
)

bolt_app = App(
    signing_secret=SLACK_SIGNING_SECRET,
    oauth_settings=oauth_settings
)
bolt_app_handler = SlackRequestHandler(bolt_app)
router = APIRouter()

@router.get("/slack/install")
async def install(req: Request):
    """
    Visit $API_HOST/slack/install in a browser to directly install slack
    """
    return await bolt_app_handler.handle(req)

@router.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await bolt_app_handler.handle(req)

@router.post("/api/v1/slack/message")
async def endpoint(req: Request):
    return await bolt_app_handler.handle(req)

@bolt_app.event("message")
def handle_message(body, say, logger):
    if 'type' in body:
        event_type = body['type']

    if event_type == 'url_verification':
        say(body['challenge'])

    if event_type == 'event_callback':
        message = SlackMessagePayload(**body)
        
        say(show_prompt())
        answer = answer_question(message.event.text)
        say(answer)

@bolt_app.event("app_mention")
def handle_app_mention(body, say):
    message = SlackMessagePayload(**body)
    
    say(show_prompt())
    answer = answer_question(preprocess_message(message.event.text))
    say(answer)

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

def postprocess_message(message: str) -> str:
    pass

def show_prompt() -> str:
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
         "Looking into it!"
    ]
    prompt_response = random.choice(prompt_responses)
    return f"{prompt_response} Please wait a few moments..."


#@router.get('/api/v1/answer_question/{question}') #TODO make an endpoint for this for the websocket app to send requests to

def answer_question(question: str):
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(PINECONE_INDEX, embedding_function)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

    rag_prompt = hub.pull("rlm/rag-prompt")
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

    answer = rag_chain.invoke(question)

    logger.debug(f"Question: {question} = Answer: {answer.content}")

    return answer.content