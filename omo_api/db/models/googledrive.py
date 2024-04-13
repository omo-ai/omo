from sqlalchemy import Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import NestedMutableJson

from omo_api.db.models.common import CommonMixin, Base, TeamMixin

class GoogleDriveConfig(CommonMixin, Base, TeamMixin):

    gdrive_id: Mapped[str] = mapped_column(unique=True, index=True)
    delegate_email: Mapped[str] = mapped_column(nullable=True)
    files = Column(NestedMutableJson)
