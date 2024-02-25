import os
import logging
from logging.config import dictConfig
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
from starlette.types import Message
from omo_api.conf.log import log_config
from omo_api.conf.auth0 import AUTH0_CORS_IPS
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
    ]
    openapi_url = '/api/v1/openapi.json'

app = FastAPI(openapi_url=openapi_url)

def log_info(req_body, res_body):
    logging.info(req_body)
    #TODO this is returning null. likely because in get_slack_user_context
    # we call request.json()
    logging.info(res_body)

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive

@app.middleware('http')
async def LogMiddleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)

app.include_router(googledrive_router.router)
app.include_router(auth_router.router)
app.include_router(files_router.router)
app.include_router(confluence_router.router)
app.include_router(slack_router.router)


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
