from sqlalchemy import select, Boolean, Column, ForeignKey, Integer, BigInteger, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from omo_api.db.models.common import CommonMixin, Base, TeamMixin

class GoogleDriveConfig(CommonMixin, Base, TeamMixin):

    delegate_email: Mapped[str] = mapped_column(nullable=True)

class GDriveObject(CommonMixin, Base):

    gdrive_id: Mapped[str] = mapped_column(unique=True, index=True)
    service_id: Mapped[str]
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str]
    last_edited_utc: Mapped[int] = mapped_column(BigInteger)
    url: Mapped[str]
    size_bytes: Mapped[str]
    last_synced_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)