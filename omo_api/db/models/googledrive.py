from sqlalchemy import select, Boolean, Column, ForeignKey, Integer, BigInteger, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..connection import Base

class GDriveObject(Base):
    __tablename__ = "gdrive_object"

    id = Column(Integer, primary_key=True, index=True)
    gdrive_id = Column(String,  unique=True, index=True)
    service_id = Column(String)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    type = Column(String)
    last_edited_utc = Column(BigInteger)
    url = Column(String)
    size_bytes = Column(String)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())