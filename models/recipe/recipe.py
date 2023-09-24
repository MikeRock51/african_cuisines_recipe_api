#!/usr/bin/env python3
"""Recipe Utils Module"""

from sqlalchemy import Column, Integer


class RecipeUtils:
    """Utility functions and attributes for recipe"""

    _prep_time_minutes = Column(Integer, nullable=False)
    _cook_time_minutes = Column(Integer, nullable=False)

    @property
    def prep_time_minutes(self) -> int:
        """Prep time getter"""
        return self._prep_time_minutes

    @prep_time_minutes.setter
    def prep_time_minutes(self, value: int) -> None:
        """Prep time setter"""
        self._prep_time_minutes = value

    @property
    def cook_time_minutes(self) -> int:
        """Cook time getter"""
        return self._cook_time_minutes

    @cook_time_minutes.setter
    def cook_time_minutes(self, value: int) -> None:
        """Cook time setter"""
        self._cook_time_minutes = value
