from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omo_api.db.models.common import Base, CommonMixin, TeamMixin

class AtlassianConfig(CommonMixin, Base, TeamMixin):

    username: Mapped[str]
    api_key: Mapped[str] # hashed

    space_keys: Mapped[List['ConfluenceSpaceKey']] = relationship(back_populates='configs')
    team: Mapped['Team'] = relationship(back_populates='atlassian_configs')

class ConfluenceSpaceKey(CommonMixin, Base):
    
    space_key: Mapped[str] = mapped_column(index=True)

    config_id: Mapped[int] = mapped_column(ForeignKey("atlassianconfig.id"))
    configs: Mapped['AtlassianConfig'] = relationship(back_populates='space_keys') 
    confluence_objs: Mapped[List['ConfluenceObject']] = relationship(back_populates='spaces')

class ConfluenceObject(CommonMixin, Base):

    confluence_id: Mapped[int] = Mapped[str]
    title: Mapped[str]
    source: Mapped[str]

    space_id: Mapped[int] = mapped_column(ForeignKey("confluencespacekey.id"))
    spaces: Mapped['ConfluenceSpaceKey'] = relationship(back_populates='confluence_objs')