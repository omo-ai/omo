import os
import logging
from logging.config import dictConfig
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import Settings
from omo_api.conf.log import log_config
from omo_api.routers import (
    # avoid naming collisions with models
    auth as auth_router,
    chats as chat_router,
    confluence as confluence_router,
    connectors as connectors_router,
    files as files_router,
    google_drive as google_drive_router,
    notion as notion_router,
    qa as qa_router,
    slack as slack_router,
    users as user_router,
)
from omo_api.db.connection import engine
from omo_api.settings import CORS_ORIGINS, OPENAPI_URL
from omo_api.utils import get_env_var, valid_api_token, configure_apm

# Necessary for the call to create_all() to create tables
from omo_api.db.models import *


dictConfig(log_config)
logger = logging.getLogger(__name__)

configure_apm()

app = FastAPI(openapi_url=OPENAPI_URL)

router_deps = [
    # Depends(valid_api_token),
]
app.include_router(google_drive_router.router, dependencies=router_deps)
app.include_router(auth_router.router, dependencies=router_deps)
app.include_router(files_router.router, dependencies=router_deps)
app.include_router(confluence_router.router, dependencies=router_deps)
app.include_router(slack_router.router, dependencies=router_deps)
app.include_router(qa_router.router, dependencies=router_deps)
app.include_router(user_router.router, dependencies=router_deps)
app.include_router(chat_router.router, dependencies=router_deps)
app.include_router(connectors_router.router, dependencies=router_deps)
app.include_router(notion_router.router, dependencies=router_deps)


Base.metadata.create_all(bind=engine)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
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
