from sqlalchemy import Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from omo_api.db.models.common import CommonMixin, Base, TeamMixin

class GoogleDriveConfig(CommonMixin, Base, TeamMixin):

    gdrive_id: Mapped[str] = mapped_column(unique=True, index=True)
    delegate_email: Mapped[str] = mapped_column(nullable=True)
    files = Column(mutable_json_type(dbtype=JSONB, nested=True), default=lambda: {})
    team: Mapped['Team'] = relationship(back_populates='googledrive_configs')
