import os
import logging
import requests
from fastapi import FastAPI, WebSocket
from logging.config import dictConfig
from conf.log import log_config

dictConfig(log_config)
logger = logging.getLogger(__name__)

app = FastAPI()

SLACK_WEBHOOKS = {
    'omoai': {
        'hook_url': 'https://hooks.slack.com/services/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',
        'description': 'Posts to OmoAI app channel'
    }
}

@app.get("/")
async def root():
    return {"message": "Hello, Omo!"}

