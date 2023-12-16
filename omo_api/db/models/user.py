from typing import List
from sqlalchemy import select, Boolean, Column, ForeignKey, Integer, BigInteger, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from omo_api.db.models.common import CommonMixin, Base, TeamMixin
from omo_api.db.models.confluence import AtlassianConfig
from omo_api.db.models.googledrive import GoogleDriveConfig
from omo_api.db.models.pinecone import PineconeConfig



class Team(Base, CommonMixin):
    name: Mapped[str]
    slug: Mapped[str]
    is_active: Mapped[bool]

    members: Mapped[List['User']] = relationship(back_populates='members')
    team_config: Mapped[List['TeamConfig']] = relationship(back_populates='team_configs')

class TeamConfig(CommonMixin, Base):
    
    atlassian_configs: Mapped[List['AtlassianConfig']] = relationship(back_populates='atlassianconfig')
    gdrive_configs: Mapped[List['GoogleDriveConfig']] = relationship(back_populates='gdriveconfig')
    pinecone_configs: Mapped[List['PineconeConfig']] = relationship(back_populates='pineconeconfig')

    slack_team_id: Mapped[str]

    
class User(CommonMixin, Base, TeamMixin):
    __tablename__ = "users" # avoid collision with postgres schema user
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    hashed_password: Mapped[str]
    last_login: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)