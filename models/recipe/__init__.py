#!/usr/bin/env python3
"""The recipe model"""

from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import BaseModel, Base
from models.recipe.recipe import RecipeUtils
from models.utils import Utils
from sqlalchemy.orm import relationship


class Recipe(BaseModel, Base, RecipeUtils):
    """Defines a food object"""

    __tablename__ = "recipes"

    name = Column(String(255), nullable=False)
    cuisine = Column(String(128), default="Unspecified", nullable=False)
    ingredients = relationship('Ingredient', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    instructions = relationship('Instruction', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    videoInstructions = relationship('VideoInstruction', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    serving_size = Column(Integer, nullable=True)
    total_time_minutes = Column(Integer, nullable=False)
    calories_per_serving = Column(Integer, nullable=True)
    reviews = relationship('Review', backref='recipe', cascade='all, delete-orphan')
    upvotes = relationship('Upvote', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    nutritional_values = relationship('NutritionalValue', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    dps = relationship('RecipeDP', backref='recipe', cascade='all, delete-orphan', single_parent=True)
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)

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
