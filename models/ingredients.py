#!/usr/bin/env python3
"""The ingredients module"""

from sqlalchemy import Column, String


class Ingredients(BaseModel, Base):
    """Defines an ingredient object"""
    # Column(String(512)
