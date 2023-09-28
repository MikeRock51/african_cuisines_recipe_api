#!/usr/bin/env python3
"""The recipe module"""

from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from models.base_model import BaseModel, Base
from models.recipe.recipe import RecipeUtils


class Recipe(BaseModel, Base, RecipeUtils):
    """Defines a food object"""

    __tablename__ = "recipes"

    name = Column(String(255), nullable=False)
    cuisine = Column(String(128), default="Not specified", nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    serving_size = Column(Integer, nullable=True)
    total_time_minutes = Column(Integer, nullable=False)
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize instance"""
        super().__init__(*args, **kwargs)
        self.total_time_minutes = self.cook_time_minutes + self.prep_time_minutes
