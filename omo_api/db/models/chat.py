from datetime import datetime
from typing import List
from sqlalchemy import Column, ARRAY, String, DateTime, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from omo_api.db.models.common import CommonMixin, Base
from omo_api.db.models.user import User 


class Chat(CommonMixin, Base):
    chat_id: Mapped[str] # the nanoid for the chat
    title: Mapped[str] = mapped_column(String, nullable=True)
    messages = Column(mutable_json_type(dbtype=JSONB, nested=True), default=lambda: {})
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship()