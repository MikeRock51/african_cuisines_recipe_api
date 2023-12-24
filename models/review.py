#!/usr/bin/env python3
"""Review Module"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Defines a review object"""
    title = Column(String(60), nullable=True)
    description = Column(String(1024), nullable=False)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
