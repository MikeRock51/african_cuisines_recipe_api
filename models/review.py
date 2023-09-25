#!/usr/bin/env python3
"""Review Module"""

from sqlalchemy import Column, String, Integer
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Defines a review object"""
    pass
