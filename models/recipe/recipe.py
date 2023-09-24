#!/usr/bin/env python3
"""Recipe Utils Module"""

from sqlalchemy import Column, Integer


class RecipeUtils:
    """Utility functions and attributes for recipe"""

    _total_time_minutes = Column(Integer, nullable=False)
    _prep_time_minutes = Column(Integer, nullable=False)
    _cook_time_minutes = Column(Integer, nullable=False)

    @property
    def total_time_minutes(self) -> int:
        """Total time minutes getter"""
        return self._total_time_minutes

    @total_time_minutes.setter
    def total_time_minutes(self) -> None:
        """Total time minutes setter"""
        self._total_time_minutes = self._prep_time_minutes + self._cook_time_minutes

    @property
    def prep_time_minutes(self) -> int:
        """Prep time getter"""
        return self._prep_time_minutes

