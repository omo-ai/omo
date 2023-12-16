import os
import pinecone
import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from slack_sdk import WebClient
from omo_api.conf.log import log_config
from omo_api.models.slack import SlackPayload
from omo_api.routers import (
    auth_router,
    files_router, 
    googledrive_router,
    confluence_router,
    slack_router,
)
from omo_api.db.connection import engine
from omo_api.db.models.common import DeclarativeBase

# Necessary for the call to create_all() to create tables
from omo_api.db.models import *

dictConfig(log_config)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(googledrive_router.router)
app.include_router(auth_router.router)
app.include_router(files_router.router)
app.include_router(confluence_router.router)
app.include_router(slack_router.router)

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
