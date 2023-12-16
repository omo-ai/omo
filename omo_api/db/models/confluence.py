from typing import List, Optional
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, String, Integer, BigInteger, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omo_api.db.models.common import Base, CommonMixin, TeamMixin

class AtlassianConfig(CommonMixin, Base, TeamMixin):

    username: Mapped[str]
    api_key: Mapped[str] # hashed

    space_keys: Mapped[List['ConfluenceSpaceKey']] = relationship()


class ConfluenceSpaceKey(CommonMixin, Base):
    
    space_key: Mapped[str] = mapped_column(index=True)

    config_id: Mapped[int] = mapped_column(ForeignKey("atlassianconfig.id"))
    confluence_objs: Mapped[List['ConfluenceObject']] = relationship()

class ConfluenceObject(CommonMixin, Base):

    confluence_id: Mapped[int] = Mapped[str]
    title: Mapped[str]
    source: Mapped[str]

    space_id: Mapped[int] = mapped_column(ForeignKey("confluencespacekey.id"))