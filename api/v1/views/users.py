#!/usr/bin/env python3
"""User view routes"""

from flask import jsonify
from models.user import User
from models import storage
from api.v1.views import app_views
from typing import List


@app_views.route('/users')
def allUsers():
    """Retrives a list of all users from database"""
    users: List[User] = storage.all(User).values()
    print(users)

    return jsonify([user.toDict() for user in users]), 200
