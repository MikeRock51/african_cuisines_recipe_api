#!/usr/bin/env python3
"""The user module"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from models.user.auth import UserAuth


class User(BaseModel, Base, UserAuth):
    """Defines a user object"""

    __tablename__ = 'users'

    username = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    firstname = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
