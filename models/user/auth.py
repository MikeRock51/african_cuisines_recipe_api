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

    def validatePassword(self, password: str) -> bool:
        """Validates that user password matches the set password"""
        if type(password).__name__ == 'str':
            return bcrypt.checkpw(password.encode('utf-8'), self._password.encode('utf-8'))

