from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union

# Sample Websockets Payload:
# {'blocks': [{'block_id': 'i9snn',
#              'elements': [{'elements': [{'text': 'What is Aperture?',
#                                          'type': 'text'}],
#                            'type': 'rich_text_section'}],
#              'type': 'rich_text'}],
#  'channel': 'CHANNEL_ID',
#  'channel_type': 'channel',
#  'client_msg_id': 'MSG_ID',
#  'event_ts': '1702540537.014409',
#  'team': 'TEAM_ID',
#  'text': 'What is Aperture?',
#  'ts': '1702540537.014409',
#  'type': 'message',
#  'user': 'USER_ID'}


# Sample Events API Payload message event
# {
#     "token": "abc123",
#     "team_id": "TEAM_ID",
#     "context_team_id": "TEAM_ID",
#     "context_enterprise_id": null,
#     "api_app_id": "API_APP_ID",
#     "event": {
#         "client_msg_id": "f7e40963-b186-4d32-b284-2d8a4b530e3e",
#         "type": "message",
#         "text": "Hello World",
#         "user": "USER_ID",
#         "ts": "1703165690.914109",
#         "blocks": [
#             {
#                 "type": "rich_text",
#                 "block_id": "OEqvo",
#                 "elements": [
#                     {
#                         "type": "rich_text_section",
#                         "elements": [
#                             {
#                                 "type": "text",
#                                 "text": "Hello World"
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ],
#         "team": "TEAM_ID",
#         "channel": "CHANNEL_ID",
#         "event_ts": "1703165690.914109",
#         "channel_type": "channel"
#     },
#     "type": "event_callback",
#     "event_id": "Ev06B8QVF8KW",
#     "event_time": 1703165690,
#     "authorizations": [
#         {
#             "enterprise_id": null,
#             "team_id": "TEAM_ID",
#             "user_id": "USER_ID2",
#             "is_bot": true,
#             "is_enterprise_install": false
#         }
#     ],
#     "is_ext_shared_channel": false,
#     "event_context": "4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDY1TFBLMlkxSCIsImFpZCI6IkEwNjZWUThFUFY1IiwiY2lkIjoiQzA2N0hIMUJaTTMifQ"
# }


# Sample app_mention event
# {
#     "token": "abc123",
#     "team_id": "TEAM_ID",
#     "api_app_id": "API_APP_ID",
#     "event": {
#         "client_msg_id": "35870E4D-9257-4C08-A31A-0C9F540EF869",
#         "type": "app_mention",
#         "text": "<@USER_ID2> hello",
#         "user": "USER_ID",
#         "ts": "1703553410.763499",
#         "blocks": [
#             {
#                 "type": "rich_text",
#                 "block_id": "C0u85",
#                 "elements": [
#                     {
#                         "type": "rich_text_section",
#                         "elements": [
#                             {
#                                 "type": "user",
#                                 "user_id": "USER_ID2"
#                             },
#                             {
#                                 "type": "text",
#                                 "text": " hello"
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ],
#         "team": "TEAM_ID",
#         "channel": "CHANNEL_ID",
#         "event_ts": "1703553410.763499"
#     },
#     "type": "event_callback",
#     "event_id": "Ev06BCJYT3M4",
#     "event_time": 1703553410,
#     "authorizations": [
#         {
#             "enterprise_id": null,
#             "team_id": "TEAM_ID",
#             "user_id": "USER_ID2",
#             "is_bot": true,
#             "is_enterprise_install": false
#         }
#     ],
#     "is_ext_shared_channel": false,
#     "event_context": "4-eyJldCI6ImFwcF9tZW50aW9uIiwidGlkIjoiVDA2NUxQSzJZMUgiLCJhaWQiOiJBMDY2VlE4RVBWNSIsImNpZCI6IkMwNjdISDFCWk0zIn0"
# }
#event -> channel_type
#  field required (type=value_error.missing)

# Sample URL Verification Payload
# {
#     "token": "token",
#     "challenge": "challenge_token",
#     "type": "url_verification"
# }



class SlackMessageEventPayload(BaseModel):
    client_msg_id: str
    type: str
    text: str
    user: str
    ts: str
    team: str
    channel: str
    event_ts: str
    channel_type: Optional[str]

"""
Note: Slack can send two different types of payloads to us
1. For URL verification (only required once)
2. The Slack message event
Slack will send either type of payload. Hence the optional fields
to allow for either kind
"""
class SlackMessagePayload(BaseModel):
    type: str
    token: Optional[str]
    team_id: Optional[str]
    context_team_id: Optional[str]
    context_enterprise_id: str | None = None
    api_app_id: Optional[str]
    event: Optional[SlackMessageEventPayload]
    event_id: Optional[str]
    event_time: Optional[str]
    event_context: Optional[str]
    is_ext_shared_channel: Optional[bool]

    # Initial fields when using verification
    token: Optional[str]
    challenge: Optional[str]

# WebSocket Payload
# class SlackPayload(BaseModel):
#     channel: str
#     channel_type: str
#     client_msg_id: str
#     event_ts: str
#     team: str
#     text: str
#     ts: str
#     type: str
#     user: str
