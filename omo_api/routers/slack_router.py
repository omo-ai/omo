import os
import time
import json
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
    # answer_question,
    preprocess_message,
    show_prompt
)

logger = logging.getLogger(__name__)

# These need to align with the Slack events we're receiving
# Required scopes and their correspending events or API calls

oauth_required_scopes = [
    "channels:read",        # api: users.conversations
    "channels:history",     # event: message,message.channels
    "groups:read",          # api: users.conversations
    "groups:history",       # event: message
    "chat:write",           # api: chat.postMessage
    "app_mentions:read",    # event: app_mention
    "reactions:read",       # event: reaction_added, reaction_removed; api: reactions.get, reactions.list
    "im:history",           # event: message,message.im
    "mpim:history",         # event: message
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

def create_slack_response(answer, sources) -> list:
    """
    Formats the answer and sources in using Slack blocks
    """
    def format_source_str(sources) -> str:
        """
        Format the source documents
        """
        sources_str = ""

        for source in sources: # [{'title': 'Document Title', 'source': 'https://link_to_source.com'}]
            source_str = f"• <{source['source']}|{source['title']}> \n"
            sources_str += source_str

        return sources_str

    if sources:
        slack_blocks_template = [
            {
                "type": "section", # answer
                "text": {
                    "type": "mrkdwn",
                    "text": answer,
                }
            },
            {
                "type": "section", # sources
                "text": {
                    "type": "mrkdwn",
                    "text": "Sources:\n" + format_source_str(sources)
                }
            }
        ]
    else:
        slack_blocks_template = [
           {
                "type": "section", # answer
                "text": {
                    "type": "mrkdwn",
                    "text": answer,
                }
            } 
        ]
    
    return slack_blocks_template

@router.post('/api/v1/slack/answer')
async def answer_slack(body: SlackMessagePayload,
                       user_context: Annotated[dict, Depends(get_slack_user_context)]):
    start = time.time()

    logger = logging.getLogger('answer_question')
    logger.debug("---Start---")

    # dict with question, answer, and sources
    answer = answer_question(body.event.text, user_context)

    slack_response = create_slack_response(answer['answer'], answer['sources'])

    logger.debug(f"QuestionAnswer: {answer}")
    logger.debug(f"SlackUser: {user_context['slack_user_id']}")
    logger.debug(f"SlackTeam: {user_context['slack_team_id']}")
    logger.debug(f"OmoUserID: {user_context['omo_user_id']}")
    logger.debug(f"OmoTeamID: {user_context['omo_team_id']}")
    logger.debug(f"PineconeIndex: {user_context['omo_pinecone_index']}")
    
    time_elapsed = time.time() - start 
    logger.debug(f"Elapsed: {time_elapsed}")
    logger.debug("---End---")

    return slack_response

@bolt_app.event("message")
def handle_message(body, say, logger):

    if 'type' in body:
        event_type = body['type']

    if event_type == 'url_verification':
        say(body['challenge'])

    if event_type == 'event_callback':
        say(show_prompt())

        # make an HTTP request
        answer = requests.post(f"{API_HOST}/api/v1/slack/answer", json.dumps(body))

        say(blocks=answer.json(), unfurl_links=False, unfurl_media=False)

@bolt_app.event("app_mention")
def handle_app_mention(body, say):
    say(show_prompt())

    answer = requests.post(f"{API_HOST}/api/v1/slack/answer", json.dumps(body))

    say(blocks=answer.json(), unfurl_links=False, unfurl_media=False)

# TODO
@bolt_app.command("/omo")
def handle_some_command(ack, body, logger):
    ack()
    logger.info(body)
