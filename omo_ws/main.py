import os
import random
import json
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
API_HOST = os.environ['API_HOST']

# Initializes app with the bot token and socket mode handler
bolt_app = App(token=SLACK_BOT_TOKEN)

message_body = {
    "token": "abc123",
    "team_id": "TEAM_ID",
    "context_team_id": "TEAM_ID",
    "context_enterprise_id": None,
    "api_app_id": "API_APP_ID",
    "event": {
        "client_msg_id": "f7e40963-b186-4d32-b284-2d8a4b530e3e",
        "type": "message",
        "text": "Hello World",
        "user": "USER_ID",
        "ts": "1703165690.914109",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "OEqvo",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "Hello World"
                            }
                        ]
                    }
                ]
            }
        ],
        "team": "TEAM_ID",
        "channel": "CHANNEL_ID",
        "event_ts": "1703165690.914109",
        "channel_type": "channel"
    },
    "type": "event_callback",
    "event_id": "Ev06B8QVF8KW",
    "event_time": 1703165690,
    "authorizations": [
        {
            "enterprise_id": None,
            "team_id": "TEAM_ID",
            "user_id": "USER_ID2",
            "is_bot": True,
            "is_enterprise_install": True
        }
    ],
    "is_ext_shared_channel": False,
    "event_context": "4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDY1TFBLMlkxSCIsImFpZCI6IkEwNjZWUThFUFY1IiwiY2lkIjoiQzA2N0hIMUJaTTMifQ"
}

@bolt_app.event("message")
def say_hello(body, say, logger):
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
        "Good question! Let me see."
    ]
    message = body['event']['text']
    # The payload sent to a websocket endpoint is different
    # from that sent to an HTTP endpoint. Herw we mock the payload
    # sent to the HTTP endpoint with the message
    message_body['event']['text'] = message
    message_body['event']['blocks'][0]['elements'][0]['elements'][0]['text'] = message

    prompt_response = random.choice(prompt_responses)
    say(f"{prompt_response} Please wait a few moments...")
    response = requests.post(f'http://{API_HOST}/api/v1/slack/answer', json.dumps(message_body))

    say(response.text)

# Start the Slack bolt app to interact via websockets
SocketModeHandler(bolt_app, SLACK_APP_TOKEN).start()