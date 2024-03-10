import os
import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from omo_api.conf.log import log_config
from omo_api.conf.auth0 import AUTH0_CORS_IPS
from omo_api.routers import (
    auth_router,
    files_router, 
    googledrive_router,
    confluence_router,
    slack_router,
    qa,
)
from omo_api.db.connection import engine

# Necessary for the call to create_all() to create tables
from omo_api.db.models import *

dictConfig(log_config)
logger = logging.getLogger(__name__)

APP_ENV = os.getenv('APP_ENV', 'development')

if APP_ENV == 'production':
    origins = [
        "https://api.omo.bot",
        "https://app.helloomo.ai",
    ] + AUTH0_CORS_IPS
    openapi_url = None # don't publish docs publicly
else:

    origins = [
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    openapi_url = '/api/v1/openapi.json'

app = FastAPI(openapi_url=openapi_url)

app.include_router(googledrive_router.router)
app.include_router(auth_router.router)
app.include_router(files_router.router)
app.include_router(confluence_router.router)
app.include_router(slack_router.router)
app.include_router(qa.router)


Base.metadata.create_all(bind=engine)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, Omo!"}
