#!/usr/bin/env python3
"""User view routes"""

from flask import jsonify, g, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views
from typing import Dict
from api.v1.utils.authWrapper import login_required
from models.roles import UserRole
from api.v1.utils import Utils
from sqlalchemy.exc import IntegrityError
from api.v1.auth import auth
from flasgger.utils import swag_from
import os

DOCS_DIR = os.path.abspath('api/v1/views/documentations/users')

@app_views.route('/users')
@swag_from(f'{DOCS_DIR}/all_users.yml')
@login_required([UserRole.admin])
def allUsers():
    """Retrieves a list of all users from database"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)

    try:
        usersData: Dict[User] = storage.getPaginatedData(obj=User,
                                                         page=int(page))
        return jsonify(Utils.successResponse(usersData, detailed, 'users')), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app_views.route('/users', methods=['POST'])
@swag_from(f'{DOCS_DIR}/post_users.yml')
def createUser():
    """Creates a news user"""
    requiredFields = ['username', 'email', 'password']
    userFields = ['username', 'email', 'password', 'firstname', 'lastname']
    detailed = request.args.get('detailed', True)
    try:
        data = Utils.getReqJSON(request, requiredFields)
        userData = {key: value for key,
                    value in data.items() if key in userFields}
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
@swag_from(f'{DOCS_DIR}/get_me.yml')
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
@swag_from(f'{DOCS_DIR}/get_user.yml')
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

@app_views.route('/users/<id>', methods=['PUT'])
@swag_from(f'{DOCS_DIR}/put_users.yml')
@login_required()
def updateUser(id):
    """Updates a user based on user id"""
    data = Utils.getReqJSON(request)
    if not data:
        abort(400)

    user = storage.get(User, id)

    if not user:
        abort(404)
    if user is not g.currentUser:
        abort(401)

    updatables = ['username', 'firstname', 'lastname', 'password']

    try:
        for key, value in data.items():
            if key in updatables:
                setattr(user, key, value)
        user.save()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        })

    return jsonify({
        "status": "success",
        "message": "User updated successfully",
        "data": user.toDict(detailed=True)
    }), 200


@app_views.route('/users/<id>', methods=['DELETE'])
@login_required()
def deleteUser(id):
    """Deletes the user with the user id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    if user is not g.currentUser:
        abort(401)
    try:
        user.delete()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        })

    return jsonify({
        "status": "success",
        "message": "User deleted sucessfully"
    })
