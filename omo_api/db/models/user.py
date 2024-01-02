from typing import List
from sqlalchemy import ARRAY, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from omo_api.db.models.common import CommonMixin, Base, TeamMixin
from omo_api.db.models.confluence import AtlassianConfig
from omo_api.db.models.googledrive import GoogleDriveConfig
from omo_api.db.models.pinecone import PineconeConfig

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
    team_config: Mapped[List['TeamConfig']] = relationship(back_populates='team')

class TeamConfig(CommonMixin, Base):
    
    atlassian_configs: Mapped[List['AtlassianConfig']] = relationship(back_populates='team_configs')
    gdrive_configs: Mapped[List['GoogleDriveConfig']] = relationship(back_populates='team_configs')
    pinecone_configs: Mapped[List['PineconeConfig']] = relationship(back_populates='team_configs')

    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    team: Mapped['Team'] = relationship(back_populates='team_config')