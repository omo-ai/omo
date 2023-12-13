from typing import List, Optional
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, String, Integer, BigInteger, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from omo_api.db.connection import Base

class AtlassianConfig(Base):
    __tablename__ = "atlassian_configs"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str]
    api_key: Mapped[str]

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    space_keys: Mapped[List['ConfluenceSpaceKey']] = relationship()


class ConfluenceSpaceKey(Base):
    __tablename__ = "confluence_space_keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    space_key: Mapped[str] = mapped_column(index=True)

    config_id: Mapped[int] = mapped_column(ForeignKey("atlassian_configs.id"))
    confluence_objs: Mapped[List['ConfluenceObject']] = relationship()

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ConfluenceObject(Base):
    __tablename__ = "confluence_objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    confluence_id: Mapped[int] = Mapped[str]
    title: Mapped[str]
    source: Mapped[str]

    space_id: Mapped[int] = mapped_column(ForeignKey("confluence_space_keys.id"))

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
