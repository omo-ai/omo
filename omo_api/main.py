import os
import pinecone
import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from slack_sdk import WebClient
from conf.log import log_config
from routers import googledrive
from db.connection import Base, engine, session

dictConfig(log_config)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV"), 
)

app = FastAPI()
app.include_router(googledrive.router)

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

SLACK_WEBHOOKS = {
    'omoai': {
        'hook_url': 'https://hooks.slack.com/services/TEAM_ID/B067CPYU8TW/3ZYuK7PRpPMrqbAeIsDGxNUc',
        'description': 'Posts to OmoAI app channel'
    }
}

@app.get("/")
async def root():
    return {"message": "Hello, Omo!"}


@app.get('/api/v1/answer_question/{question}')
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

@app.get('/api/v1/slack/oauth2_redirect')
async def post_install(code: str):
    logger.debug(f"slack temp auth code received: {code}")

    if code:
        client = WebClient()

        response = client.oauth_v2_access(
            client_id=SLACK_CLIENT_ID,
            client_secret=SLACK_CLIENT_SECRET,
            code=code,
        )
        logger.debug("oauth2 response", response)

        is_enterprise_install = response.get('is_enterprise_install', False)
    else:
        pass

    # TODO save to database
    os.environ["SLACK_BOT_TOKEN"] = response['access_token']
    
    message = "Connected to Slack. You may close this page"
    return message