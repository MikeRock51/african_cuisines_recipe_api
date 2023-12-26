#!/usr/bin/env python3
"""The ingredients module"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import relationship


class Ingredient(BaseModel, Base):
    """Defines an ingredient object"""

    __tablename__ = "ingredients"

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    quantity = Column(Integer, nullable=True)
    dps = relationship('IngredientDP', backref='ingredient', cascade='all, delete-orphan', single_parent=True)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    UniqueConstraint('name', 'recipeID', name='uq_igd_per_recipe')
