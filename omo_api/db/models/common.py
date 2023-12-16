from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    declared_attr,
    DeclarativeBase,
    relationship
)

class Base(DeclarativeBase):
    pass

class CommonMixin:

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class TeamMixin:

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    @declared_attr
    def team(cls) -> Mapped['Team']:
        return relationship(back_populates="team")
