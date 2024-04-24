import enum
from typing import List
from sqlalchemy import Column, ARRAY, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy.dialects.postgresql import JSONB

from omo_api.db.models.common import CommonMixin, Base
from omo_api.db.models.confluence import AtlassianConfig
from omo_api.db.models.googledrive import GoogleDriveConfig
from omo_api.db.models.pinecone import PineconeConfig
from omo_api.settings import cipher_suite


class User(CommonMixin, Base):
    __tablename__ = "users" # avoid collision with postgres schema user
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    hashed_password: Mapped[str]
    last_login: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    slack_user_profile: Mapped['SlackProfile'] = relationship(back_populates='user')

    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'), nullable=True)
    team: Mapped['Team'] = relationship(back_populates='users') # user can belong to a team


class Team(Base, CommonMixin):
    name: Mapped[str]
    slug: Mapped[str]
    is_active: Mapped[bool]
    domains: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)

    slack_team_id: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[List['User']] = relationship(back_populates='team')

    atlassian_configs: Mapped[List['AtlassianConfig']] = relationship(back_populates='team')
    googledrive_configs: Mapped[List['GoogleDriveConfig']] = relationship(back_populates='team')
    pinecone_configs: Mapped[List['PineconeConfig']] = relationship(back_populates='team')


class UserCeleryTasks(Base, CommonMixin):
    job_id: Mapped[str] # task_id
    connector = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True) # e.g. { "googledrive": ["connector_id"] }

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship()


class UserAPIKey(Base, CommonMixin):
    api_key: Mapped[str] = Column(StringEncryptedType(String, cipher_suite))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship()