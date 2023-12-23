#!/usr/bin/env python3
"""The chat model"""

from sqlalchemy import Column, String, ForeignKey, Text
from models.base_model import BaseModel, Base

class Chat(BaseModel, Base):
    """Defines a chat object"""

    __tablename__ = "chats"

    userID = Column(String(60), ForeignKey('users.id'), nullable=False)
    sessionID = Column(String(60), ForeignKey("chat_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    role = Column(String(100), nullable=False)
