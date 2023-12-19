import os
import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware # TODO
from omo_api.conf.log import log_config
from omo_api.routers import (
    auth_router,
    files_router, 
    googledrive_router,
    confluence_router,
    slack_router,
)
from omo_api.db.connection import engine

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
 
APP_ENV = os.getenv('APP_ENV', 'development')

if APP_ENV == 'production':
    origins = [
        "https://api.omo.bot",
        "https://app.helloomo.ai",
    ]
else:

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
