#!/usr/bin/env python3
"""The instructions model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Instruction(BaseModel, Base):
    """Defines an instruction object"""

    __tablename__ = "instructions"

    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    medias = relationship('InstructionMedia', backref='instruction', cascade='all, delete-orphan, delete')
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)

    def toDict(self, detailed=False):
        """Extension of basemodel.toDict for instruction data"""
        instance = super().toDict()
        instance['instruction_medias'] = [media.toDict() for media in self.medias]
        if detailed:
            return instance

        heldBackAttrs = ["__class__", "createdAt", "updatedAt"]

        # Filter heldback attributes
        for attr in heldBackAttrs:
            if attr in instance:
                instance.pop(attr)

        return instance
