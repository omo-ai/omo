import os
import random
import requests
import logging
from logging.config import dictConfig
from omo_ws.conf.log import log_config
from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

dictConfig(log_config)
logger = logging.getLogger(__name__)

# uvicorn (in Dockerfile) needs something to run
# we can't pass it the Bolt app
app = FastAPI() 

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

# Initializes app with the bot token and socket mode handler
bolt_app = App(token=SLACK_BOT_TOKEN)

@bolt_app.event("message")
def say_hello(message, say):
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
        "Good question! Let me see."
    ]

    question = message['text']
    prompt_response = random.choice(prompt_responses)
    say(f"{prompt_response} Please wait a few moments...")
    response = requests.get(f'http://omo_server_1/api/v1/answer_question/{question}')

    say(response.text)

# Start the Slack bolt app to interact via websockets
SocketModeHandler(bolt_app, SLACK_APP_TOKEN).start()