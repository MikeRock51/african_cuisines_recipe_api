#!/usr/bin/env python3
"""The instructions model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Ingredient(BaseModel, Base):
    """Defines an instruction object"""

    __tablename__ = "instructions"

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    medias = relationship('instructionMedia', backref='instruction', cascade='all, delete-orphan', single_parent=True)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
