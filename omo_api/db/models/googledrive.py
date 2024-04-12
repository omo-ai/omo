import datetime
from typing import List
from sqlalchemy import select, Boolean, Column, DateTime, ForeignKey, Integer, BigInteger, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import NestedMutableJson

from omo_api.db.models.common import CommonMixin, Base, TeamConfigMixin

class GoogleDriveConfig(CommonMixin, Base, TeamConfigMixin):

    gdrive_id: Mapped[str] = mapped_column(unique=True, index=True)
    delegate_email: Mapped[str] = mapped_column(nullable=True)
    #objects: Mapped[List['GDriveObject']] = relationship(back_populates='drive')

    files = Column(NestedMutableJson)