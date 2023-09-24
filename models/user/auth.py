#!/usr/bin/env python3
"""Handles user authentication"""

from sqlalchemy import Column, String
import bcrypt

class UserAuth:
    """Authenticates user"""

    _password = Column(String(128), nullable=True)

    @property
    def password(self) -> str:
        """User password getter"""

        return self._password

    @password.setter
    def password(self, pwd: str) -> None:
        """Encrypts and stores user password to database"""
        if not pwd:
            raise ValueError('Password required')

        hashedPwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        self._password = hashedPwd
