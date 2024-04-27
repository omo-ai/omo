import os
import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import Settings

from omo_api.conf.log import log_config
from omo_api.routers import (
    # avoid naming collisions with models
    auth as auth_router,
    confluence as confluence_router,
    files as files_router,
    google_drive as google_drive_router,
    slack as slack_router,
    qa as qa_router,
    user as user_router,
)
from omo_api.db.connection import engine
from omo_api.settings import CORS_ORIGINS, OPENAPI_URL
from omo_api.utils import get_env_var

# Necessary for the call to create_all() to create tables
from omo_api.db.models import *

dictConfig(log_config)
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url=OPENAPI_URL)

app.include_router(google_drive_router.router)
app.include_router(auth_router.router)
app.include_router(files_router.router)
app.include_router(confluence_router.router)
app.include_router(slack_router.router)
app.include_router(qa_router.router)
app.include_router(user_router.router)


Base.metadata.create_all(bind=engine)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


llm = get_env_var('LLM')
if llm == 'openai':
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding

    Settings.embed_model = OpenAIEmbedding(model=get_env_var('OPENAI_EMBEDDING_MODEL'))
    Settings.llm = OpenAI(temperature=0.0, model=get_env_var('OPENAI_MODEL'))

@app.get("/")
async def root():
    return {"message": "Hello, Omo!"}
