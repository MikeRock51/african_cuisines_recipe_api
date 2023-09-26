#!/usr/bin/env python3
"""Defines an authentication function decorator"""

from flask import g, abort
from functools import wraps
from models.roles import UserRole
from typing import Union, List, Callable

def login_required(authorizedRoles: Union[List[UserRole], None] = None) -> Callable:
    """Wraps routes that requires authentication"""
    def loginWrapper(f):
        @wraps(f)
        def route_function(*args, **kwargs):
            def unauthorized():
                abort(401)

            if not g.currentUser:
                return unauthorized()
            if authorizedRoles is not None and g.currentUser.role not in authorizedRoles:
                return unauthorized()

            return f(*args, **kwargs)
        return route_function
    return loginWrapper
