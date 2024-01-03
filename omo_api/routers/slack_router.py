import os
import time
import logging
import requests
from typing import Annotated
from fastapi import APIRouter, Request, Depends

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from omo_api.utils.context import get_slack_user_context
from omo_api.models.slack import SlackMessagePayload
from omo_api.routers.qa import (
    answer_question,
    preprocess_message,
    postprocess_message,
    show_prompt
)

logger = logging.getLogger(__name__)

# These need to align with the Slack events we're receiving
oauth_required_scopes = [
    "channels:read",
    "groups:read",
    "chat:write",
    "app_mentions:read",
    "reactions:read"
]

SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
API_HOST = os.getenv('API_HOST')

oauth_settings = OAuthSettings(
    client_id=SLACK_CLIENT_ID,
    client_secret=SLACK_CLIENT_SECRET,
    scopes=oauth_required_scopes,
    installation_store=FileInstallationStore(base_dir="/mnt/efs/slack/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="/mnt/efs/slack/states")
)

bolt_app = App(
    signing_secret=SLACK_SIGNING_SECRET,
    oauth_settings=oauth_settings
)
bolt_app_handler = SlackRequestHandler(bolt_app)

router = APIRouter()

@router.get("/slack/install")
async def install(req: Request):
    """
    Visit $API_HOST/slack/install in a browser to directly install slack
    """
    return await bolt_app_handler.handle(req)

@router.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await bolt_app_handler.handle(req)

@router.post("/api/v1/slack/message")
async def endpoint(req: Request):
    return await bolt_app_handler.handle(req)


@router.post('/api/v1/slack/answer')
async def answer_slack(body: SlackMessagePayload,
                       user_context: Annotated[dict, Depends(get_slack_user_context)]):
    start = time.time()

    logger = logging.getLogger('answer_question')
    logger.debug("---Start---")

    logger.debug(f"Question: {body.event.text}")

    answer = answer_question(body.event.text, user_context)

    logger.debug(f"Answer: {answer}")
    logger.debug(f"OmoUserID: {user_context['omo_user_id']}")
    
    time_elapsed = time.time() - start 
    logger.debug(f"Elapsed: {time_elapsed}")
    logger.debug("---End---")

@bolt_app.event("message")
def handle_message(body, say, logger):

    if 'type' in body:
        event_type = body['type']

    if event_type == 'url_verification':
        say(body['challenge'])

    if event_type == 'event_callback':
        say(show_prompt())

        # make an HTTP request
        answer = requests.post(f"{API_HOST}/api/v1/slack/answer", body)
        postprocessed_msg = postprocess_message(answer)

        say(postprocessed_msg)

@bolt_app.event("app_mention")
def handle_app_mention(body, say):
    message = SlackMessagePayload(**body)
    
    say(show_prompt())

    preprocessed_msg = preprocess_message(message.event.text)
    answer = answer_question(preprocessed_msg)
    postprocessed_msg = postprocess_message(answer)

    say(postprocessed_msg)

# TODO
@bolt_app.command("/omo")
def handle_some_command(ack, body, logger):
    ack()
    logger.info(body)
