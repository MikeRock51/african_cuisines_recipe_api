#!/usr/bin/env python3
"""The bookmark model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint


class Bookmark(BaseModel, Base):
    """Defines a bookmark object"""

    __tablename__ = "bookmarks"

    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    listID = Column(String(60), ForeignKey('bookmark_lists.id'), nullable=False)
    UniqueConstraint('recipeID', 'listID', name='uq_recipe_per_list')
