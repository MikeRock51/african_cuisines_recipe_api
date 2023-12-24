#!/usr/bin/env python3
"""The user module"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Enum, Integer
from models.user.auth import UserAuth
from sqlalchemy.orm import relationship
from models.roles import UserRole
from models.utils import Utils


class User(BaseModel, Base, UserAuth):
    """Defines a user object"""

    __tablename__ = 'users'

    username = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    firstname = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.contributor, nullable=False)
    recipes = relationship('Recipe', backref='author', cascade='all, delete')
    bookmark_lists = relationship('BookmarkList', backref='user', cascade='all, delete-orphan', single_parent=True)
    dp = Column(String(384), nullable=False)

    def toDict(self, detailed=False):
        """Returns a dictionary representation of a user instance"""
        instance = super().toDict()
        instance['role'] = instance['role'].value
        order = ['firstname', 'lastname', 'username', 'role', 'id']

        if detailed:
            return Utils.sortDictKeys(instance, order)

        heldBackAttrs = ['createdAt', 'updatedAt', 'email', 'role']

        for attr in heldBackAttrs:
            if attr in instance:
                instance.pop(attr)

        return Utils.sortDictKeys(instance, order)
