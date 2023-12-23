#!/usr/bin/env python3
"""The recipe model"""

from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from models.base_model import BaseModel, Base
from models.recipe.recipe import RecipeUtils
from models.utils import Utils
from sqlalchemy.orm import relationship


class Recipe(BaseModel, Base, RecipeUtils):
    """Defines a food object"""

    __tablename__ = "recipes"

    name = Column(String(255), nullable=False)
    cuisine = Column(String(128), default="Not specified", nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    serving_size = Column(Integer, nullable=True)
    total_time_minutes = Column(Integer, nullable=False)
    calories_per_serving = Column(Integer, nullable=True)
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)
    dps = relationship('RecipeDP', backref='recipe', cascade='all, delete-orphan', single_parent=True)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize instance"""
        # Initialize instace 
        super().__init__(*args, **kwargs)
        # Calculate total cook time
        self.total_time_minutes = self.cook_time_minutes \
            + self.prep_time_minutes

    def toDict(self, detailed=False):
        """Extension of basemodel.toDict for recipe data"""
        instance = super().toDict()
        order = ['name', 'cuisine', 'id', 'prep_time_minutes',
                 'cook_time_minutes', 'total_time_minutes',
                 'calories_per_serving', 'serving_size', 'userID',
                 'ingredients', 'instructions']
        instance['dps'] = [dp.toDict() for dp in self.dps]

        if detailed:
            return Utils.sortDictKeys(instance, order)

        heldBackAttrs = ["__class__", "createdAt", "updatedAt", "userID"]

        # Filter heldback attributes
        for attr in heldBackAttrs:
            if attr in instance:
                instance.pop(attr)

        return Utils.sortDictKeys(instance, order)
