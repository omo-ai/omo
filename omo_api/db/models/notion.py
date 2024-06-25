from cryptography.fernet import Fernet
from sqlalchemy import Column, ARRAY, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import EncryptedType
from omo_api.db.models.common import CommonMixin, Base, TeamMixin
from omo_api.utils import get_env_var

encryption_key = get_env_var('ENCRYPTION_KEY')

class NotionConfig(CommonMixin, Base, TeamMixin):
    oauth_token: Mapped[str] = Column(EncryptedType(String, encryption_key))
    pages = Column(mutable_json_type(dbtype=JSONB, nested=True), default=lambda: {})
    databases: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
