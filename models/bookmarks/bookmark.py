#!/usr/bin/env python3
"""The bookmark model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey


class Bookmark(BaseModel, Base):
    """Defines a bookmark object"""

    __tablename__ = "bookmarks"

    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    listID = Column(String(60), ForeignKey('bookmark_lists.id'), nullable=False)
