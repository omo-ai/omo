from typing import List
from sqlalchemy import Column, ARRAY, String, DateTime, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB
from omo_api.db.models.common import CommonMixin, Base

class Application(CommonMixin, Base):
    name: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship()
    api_keys: Mapped[List['APIKey']] = relationship()

class APIKey(Base, CommonMixin):
    hashed_api_key: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    label: Mapped[bool] = mapped_column(nullable=True)
    app_id: Mapped[int] = mapped_column(ForeignKey('application.id'), nullable=True)
    app: Mapped['Application'] = relationship(back_populates='api_keys')