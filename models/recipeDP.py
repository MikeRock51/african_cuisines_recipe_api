#!/usr/bin/env python3
"""The recipe display picture model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint


class RecipeDP(BaseModel, Base):
    """Defines a recipe DP object"""

    __tablename__ = 'recipe_dps'

    filePath = Column(String(384), nullable=False, default="https://thumbs.dreamstime.com/b/%C3%A9pices-et-vieux-livre-de-recette-33493138.jpg")
    fileType = Column(String(30), nullable=False, default="link")
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)
    UniqueConstraint('filePath', 'recipeID', name='uq_dp_per_recipe')
