import datetime
from typing import List
from sqlalchemy import select, Boolean, Column, DateTime, ForeignKey, Integer, BigInteger, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from omo_api.db.models.common import CommonMixin, Base, TeamConfigMixin

class GoogleDriveConfig(CommonMixin, Base, TeamConfigMixin):

    gdrive_id: Mapped[str] = mapped_column(unique=True, index=True)
    delegate_email: Mapped[str] = mapped_column(nullable=True)
    objects: Mapped[List['GDriveObject']] = relationship(back_populates='drive')

class GDriveObject(CommonMixin, Base):

    service_id: Mapped[str]
    object_id: Mapped[str] = mapped_column(index=True, server_default='BACKFILL')
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str]
    last_edited_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    url: Mapped[str]
    size_bytes: Mapped[str]
    last_synced_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    drive_id: Mapped[int] = mapped_column(ForeignKey('googledriveconfig.id'))
    drive: Mapped['GoogleDriveConfig'] = relationship(back_populates='objects')