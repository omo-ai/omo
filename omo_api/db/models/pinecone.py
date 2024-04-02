from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ARRAY, String
from omo_api.db.models.common import CommonMixin, Base, TeamConfigMixin

class PineconeConfig(CommonMixin, Base, TeamConfigMixin):

    index_name: Mapped[str]
    api_key: Mapped[str] # secrets manager path; not the actual key in plaintext
    environment: Mapped[str]
    namespaces: Mapped[ARRAY] = mapped_column(ARRAY(String), default=['default'])