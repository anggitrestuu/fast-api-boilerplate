from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class TestItem(Base):
    __tablename__ = "test_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
        # Add new field
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())