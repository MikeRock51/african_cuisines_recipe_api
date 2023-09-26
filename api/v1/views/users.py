#!/usr/bin/env python3
"""User view routes"""

from flask import jsonify, g
from models.user import User
from models import storage
from api.v1.views import app_views
from typing import List
from api.v1.utils.authWrapper import login_required


@app_views.route('/users')
@login_required()
def allUsers():
    """Retrives a list of all users from database"""
    users: List[User] = storage.all(User).values()

    return jsonify([user.toDict() for user in users]), 200
