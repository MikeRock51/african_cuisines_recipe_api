#!/usr/bin/env python3
"""The video instructions model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey


class VideoInstruction(BaseModel, Base):
    """Defines a video instruction object"""

    __tablename__ = "video_instructions"

    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    filePath = Column(String(500), nullable=False)
    fileType = Column(String(30), nullable=False) # link or file
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
