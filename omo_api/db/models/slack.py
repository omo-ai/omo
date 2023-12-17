from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from omo_api.db.models.common import CommonMixin, Base, TeamMixin

class SlackProfile(CommonMixin, Base):
    user_id: Mapped[str]
    team_id: Mapped[str]

    bot_access_token: Mapped[str] = mapped_column(nullable=True)
    user_access_token: Mapped[str] = mapped_column(nullable=True)
    team_name: Mapped[str] = mapped_column(nullable=True)
    team_id: Mapped[str] = mapped_column(nullable=True)
    enterprise_name: Mapped[str] = mapped_column(nullable=True)
    enterprise_id: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='slack_user_profile')

"""
6190801100051.6354667218309.013754bf6db7ea2040f889b2b63fb9bdc2bc90c7c680f0494ede2968e9ccb0ff
{
    "ok": true,
    "access_token": "***REMOVED***",
    "token_type": "bot",
    "scope": "commands,incoming-webhook",
    "bot_user_id": "U0KRQLJ9H",
    "app_id": "APP_ID",
    "team": {
        "name": "Slack Softball Team",
        "id": "T9TK3CUKW"
    },
    "enterprise": {
        "name": "slack-sports",
        "id": "E12345678"
    },
    "authed_user": {
        "id": "U1234",
        "scope": "chat:write",
        "access_token": "xoxp-1234",
        "token_type": "user"
    }
}
"""
"""
{'blocks': [{'block_id': 'i9snn',
             'elements': [{'elements': [{'text': 'What is Aperture?',
                                         'type': 'text'}],
                           'type': 'rich_text_section'}],
             'type': 'rich_text'}],
 'channel': 'CHANNEL_ID',
 'channel_type': 'channel',
 'client_msg_id': 'MSG_ID',
 'event_ts': '1702540537.014409',
 'team': 'TEAM_ID',
 'text': 'What is Aperture?',
 'ts': '1702540537.014409',
 'type': 'message',
 'user': 'USER_ID'}
"""