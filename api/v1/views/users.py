#!/usr/bin/env python3
"""User view routes"""

from flask import jsonify, g, request
from models.user import User
from models import storage
from api.v1.views import app_views
from typing import List
from api.v1.utils.authWrapper import login_required
from models.roles import UserRole
from api.v1.utils.utilities import Utilities


@app_views.route('/users')
@login_required([UserRole.admin])
def allUsers():
    """Retrives a list of all users from database"""
    users: List[User] = storage.all(User).values()
    return jsonify([user.toDict(detailed=True) for user in users]), 200

@app_views.route('/users', methods=['POST'])
def createUser():
    """Creates a news user"""
    requiredFields = ['username', 'email', 'password']
    try:
        userData = Utilities.getReqJSON(request, requiredFields)
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

