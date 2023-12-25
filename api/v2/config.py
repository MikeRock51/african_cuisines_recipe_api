#!/usr/bin/env python3
"""Defines app configs"""

from models.roles import UserRole
from api.v2.auth.session_auth import SessionAuth
from os import getenv


class Configs:
    USER_ROLES = [UserRole.admin, UserRole.moderator, UserRole.editor, UserRole.contributor, UserRole.user]

    AUTH = {
            "session": SessionAuth()
    }[getenv('AUTH_TYPE')]
