from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100))
    sender = Column(String(255))
    content = Column(Text)
    priority = Column(String(20))
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
