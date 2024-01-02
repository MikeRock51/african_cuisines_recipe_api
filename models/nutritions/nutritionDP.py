#!/usr/bin/env python3
"""The nutritional value display picture model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint


class NutritionDP(BaseModel, Base):
    """Defines a Nutrition DP object"""

    __tablename__ = 'nutrition_dps'

    filePath = Column(String(384), nullable=False)
    fileType = Column(String(30), nullable=False, default="link")
    NutritionID = Column(String(60), ForeignKey('nutritional_values.id'), nullable=False)
    UniqueConstraint('filePath', 'nutritionaID', name='uq_dp_per_nutrition')
