from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

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

class SlackPayload(BaseModel):
    channel: str
    channel_type: str
    client_msg_id: str
    event_ts: str
    team: str
    text: str
    ts: str
    type: str
    user: str