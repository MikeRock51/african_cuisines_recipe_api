#!/usr/bin/env python3
"""The bookmark list model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class BookmarkList(BaseModel, Base):
    """Defines a bookmark list object"""

    __tablename__ = "bookmark_lists"

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', 'userID', name='uq_list_per_user'),
    )
