#!/usr/bin/env python3
"""The recipe module"""

from sqlalchemy import Column, String, JSON
from models.base_model import BaseModel, Base


class Recipe(BaseModel, Base):
    """Defines a food object"""

    __tablename__ = "recipes"

    recipe_name = Column(String(255), nullable=False)
    cuisine = Column(String(128), default="Not specified", nullable=False)
    ingredients = Column(JSON, nullable=False)
