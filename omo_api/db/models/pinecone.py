from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ARRAY, String
from omo_api.db.models.common import CommonMixin, Base, TeamMixin

class PineconeConfig(CommonMixin, Base, TeamMixin):

    index_name: Mapped[str]
    api_key: Mapped[str] # hashed
    environment: Mapped[str]
    namespaces: Mapped[ARRAY] = mapped_column(ARRAY(String), default=['default'])