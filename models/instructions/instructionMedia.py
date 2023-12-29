#!/usr/bin/env python3
"""The media (picture or video) model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint


class InstructionMedia(BaseModel, Base):
    """Defines an instruction media object"""

    __tablename__ = 'instruction_medias'

    filePath = Column(String(500), nullable=False)
    fileType = Column(String(30), nullable=False) # link or file
    format = Column(String(30), nullable=False) # image or video
    InstructionID = Column(String(60), ForeignKey('instructions.id'), nullable=False)
    UniqueConstraint('filePath', 'instructionID', name='uq_media_per_instruction')
