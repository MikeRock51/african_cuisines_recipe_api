#!/usr/bin/env python3
"""User view routes"""

from flask import jsonify, g, request
from models.user import User
from models import storage
from api.v1.views import app_views
from typing import List
from api.v1.utils.authWrapper import login_required
from models.roles import UserRole
from api.v1.utils import Utils
from sqlalchemy.exc import IntegrityError
from api.v1.auth import auth


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
    userFields = ['username', 'email', 'password', 'firstname', 'lastname']
    detailed = request.args.get('detailed', False)
    try:
        data = Utils.getReqJSON(request, requiredFields)
        userData = {key: value for key, value in data.items() if key in userFields}
        user = User(**userData)
        user.save()
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(ie))
        }), 400

    return jsonify({
        "status": "success",
        "message": "Account created successfully",
        "data": user.toDict(detailed=detailed)
    }), 201

@app_views.route('/users/me')
@login_required()
def getCurrentUser():
    """Returns the current user data"""
    detailed = request.args.get('detailed', False)
    return jsonify({
        "status": "success",
        "message": "Current user retrieved successfully",
        "data": g.currentUser.toDict(detailed=detailed)
    })

@app_views.route('/users/<id>')
@login_required()
def getUserByID(id):
    """Returns a user based on user ID"""
    detailed = request.args.get('detailed', False)
    try:
        user = auth.getUserID(id)
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 404

    return jsonify({
        "status": "success",
        "message": "User retrieved successfully",
        "data": user.toDict(detailed=detailed)
    })
