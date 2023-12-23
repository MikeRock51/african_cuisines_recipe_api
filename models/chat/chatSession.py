#!/usr/bin/env python3
"""Chat session model"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class ChatSession(BaseModel, Base):
    """Defines the ChatSession schema"""
    __tablename__ = "chat_sessions"

    topic = Column(String(128), nullable=False)
    chats = relationship('Chat', backref='session', cascade='all, delete')
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize instance"""
        super().__init__(*args, **kwargs)

        if not self.topic:
            self.topic = f"Chat {self.id}"
