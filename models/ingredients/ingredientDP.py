#!/usr/bin/env python3
"""The ingredient display picture model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint


class IngredientDP(BaseModel, Base):
    """Defines an ingredient DP object"""

    __tablename__ = 'ingredient_dps'

    filePath = Column(String(384), nullable=False, default="https://thumbs.dreamstime.com/z/cuisson-faisant-cuire-le-fond-blanc-61926943.jpg?w=1400")
    fileType = Column(String(30), nullable=False, default="link")
    IngredientID = Column(String(60), ForeignKey('ingredients.id'), nullable=False)
    UniqueConstraint('filePath', 'ingredientID', name='uq_dp_per_ingredient')
