#!/usr/bin/env python3
"""Defines user roles"""

from enum import Enum


class UserRole(Enum):
    """Defines enumerated constants of user roles"""

    admin = "admin"
    moderator = "moderator"
    editor = "editor"
    contributor = "contributor"
    user = "user"

if __name__ == "__main__":
    print(UserRole.admin.value)
