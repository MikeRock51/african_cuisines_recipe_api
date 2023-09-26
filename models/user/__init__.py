#!/usr/bin/env python3
"""The user module"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Enum
from models.user.auth import UserAuth
from sqlalchemy.orm import relationship
from models.roles import UserRole


class User(BaseModel, Base, UserAuth):
    """Defines a user object"""

    __tablename__ = 'users'

    username = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    firstname = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.contributor, nullable=False)
    recipes = relationship('Recipe', backref='author', cascade='all, delete')

    def toDict(self, detailed=False):
        """Returns a dictionary representation of a user instance"""
        instance = super().toDict()
        instance['role'] = instance['role'].value

        if detailed:
            return instance

        heldBackAttrs = ['createdAt', 'updatedAt', 'email', 'role']

        for attr in heldBackAttrs:
            if attr in instance:
                instance.pop(attr)

        return instance
