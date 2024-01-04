import os
import json
from time import time, sleep

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient
from slack_bolt import App, BoltRequest, Say
from omo_api.tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from omo_api.tests.utils import (
    remove_os_env_temporarily,
    restore_os_env,
    valid_message_body
)
from omo_api.db.models.user import User, Team, TeamConfig
from omo_api.models.slack import SlackMessagePayload
from omo_api.utils.context import SlackUserContext
from omo_api.db.connection import session
from omo_api.db.models.slack import SlackProfile

class TestContext:
    signing_secret = os.getenv('SLACK_SIGNING_SECRET') 
    valid_token = os.getenv('SLACK_BOT_TOKEN')
    api_host = os.getenv('API_HOST')
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )
    db_session = session

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)
        self.valid_message_body = valid_message_body

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None
    
    def test_context_keys(self):
        # TODO assumes data is in the database
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event
            
            #TODO we should actually call answer_question instead of 
            # using a mock response. Doing so will lead to an exception
            # due to RunnableParralel
            payload = SlackMessagePayload(**body)
            ctx = SlackUserContext(payload, self.db_session)
            
            context = ctx.get_context()
            assert type(context) == dict
            assert context['omo_slack_profile_id'] == None
            assert context['omo_user_id'] == None
            assert context['omo_team_id'] == None
            assert context['omo_team_config_id'] == None
            assert context['omo_pinecone_index'] == 'starter_index'
            assert context['omo_pinecone_api_key'] == '/aws/secretsmanager/path'
            assert context['omo_pinecone_env'] == 'gcp-starter'
            assert context['slack_team_id'] == None
            assert context['slack_user_id'] == None
            say('Finished')


        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1


    def test_slack_context(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event

            payload = SlackMessagePayload(**body)
            ctx = SlackUserContext(payload, self.db_session)

            slack_profile = ctx.slack_profile_context()
            context = ctx.get_context()

            assert type(slack_profile) == SlackProfile
            assert context['omo_slack_profile_id'] != None
            assert context['slack_team_id'] != None
            assert context['slack_user_id'] != None
            say('Finished')

    
        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1
    
    def test_team_context(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event

            payload = SlackMessagePayload(**body)
            ctx = SlackUserContext(payload, self.db_session)

            ctx.team_context()
            context = ctx.get_context()

            assert context['omo_team_id'] != None
            say('Finished')
    
        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1
    
    def test_team_config(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event

            payload = SlackMessagePayload(**body)
            ctx = SlackUserContext(payload, self.db_session)

            team = ctx.team_context()
            team_config = ctx.team_config_context(team)
            context = ctx.get_context()

            assert type(team_config) == TeamConfig
            assert context['omo_team_config_id'] != None
            say('Finished')
    
        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1
    
    def test_user_context(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event

            payload = SlackMessagePayload(**body)
            ctx = SlackUserContext(payload, self.db_session)

            team = ctx.team_context()
            slack_profile = ctx.slack_profile_context()
            user = ctx.user_context(team, slack_profile)
            context = ctx.get_context()

            assert type(user) == User
            assert context['omo_user_id'] != None

            say('Finished')
    
        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1
