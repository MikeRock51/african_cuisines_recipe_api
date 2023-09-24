#!/usr/bin/env python3
"""The recipe module"""

from sqlalchemy import Column, String, JSON, Integer
from models.base_model import BaseModel, Base


class Recipe(BaseModel, Base):
    """Defines a food object"""

    __tablename__ = "recipes"

    recipe_name = Column(String(255), nullable=False)
    cuisine = Column(String(128), default="Not specified", nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    serving_size = Column(Integer, nullable=True)
    calories_per_serving = Column(Integer, nullable=True)
    prep_time_minutes = Column(Integer, nullable=False)
    cook_time_minutes = Column(Integer, nullable=False)

    def calculateTotalTime(self):
        """Returns the sum of prep time and cook time for a recipe instance"""
        return self.prep_time_minutes + self.cook_time_minutes

    total_time_minutes = Column(Integer, default=calculateTotalTime, nullable=False)
