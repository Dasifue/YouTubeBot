from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Text, DateTime, Column
from sqlalchemy.orm import DeclarativeBase

from enum import Enum

import datetime

class MessageStatus(Enum):
    InQueue = "in queue"
    Readed = "readed"
    Answered = "answered"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    full_name = Column(String(255))
    registered = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.id}//{self.telegram_id}: {self.username}"



class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("user.telegram_id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(255), nullable=False, default=MessageStatus.InQueue)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.id}//{self.user_tg_id}//{self.text}"

