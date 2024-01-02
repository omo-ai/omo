import os
import re
import json
import requests
from time import time, sleep

import pytest
from typing import Annotated
from fastapi import APIRouter, Request, Depends
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient
from slack_bolt import App, BoltRequest, Say
from omo_api.tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from omo_api.tests.utils import remove_os_env_temporarily, restore_os_env
from omo_api.routers.qa import postprocess_message

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

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

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
    
    valid_message_body = {
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
    def test_customer_context(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)

        @app.event('message')
        def handle_message(body, say, payload, event):
            assert body == self.valid_message_body
            assert body["event"] == payload
            assert payload == event
            
            #TODO we should actually call answer_question instead of 
            # using a mock response. Doing so will lead to an exception
            # due to RunnableParralel
            answer = requests.post(f"{self.api_host}/api/v1/slack/answer", json=body)
            print('*******', answer)
            #answer = postprocess_message(answer)
            #say(answer)


        timestamp, body = str(int(time())), json.dumps(self.valid_message_body)
        request: BoltRequest = BoltRequest(
            body=body, headers=self.build_headers(timestamp, body)
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

        answer = requests.post('/api/v1/slack/answer')