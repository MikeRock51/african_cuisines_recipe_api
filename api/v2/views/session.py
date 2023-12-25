#!/usr/bin/env python3
"""Handles user session"""

from flask import request, jsonify
from api.v2.views import app_views
from api.v2.auth import auth
from api.v2.utils import Utils
from models import storage
from models.user import User
from dotenv import load_dotenv
from os import getenv, path
from flasgger.utils import swag_from

load_dotenv()
DOCS_DIR = path.dirname(__file__) + '/documentations/session'


@app_views.route('/login', methods=['POST'])
@swag_from(f'{DOCS_DIR}/login.yml')
def userLogin():
    """Creates a user session"""
    requiredFields = ['email', 'password']
    detailed = request.args.get('detailed', False)
    try:
        credential = Utils.getReqJSON(request, requiredFields)
        user = auth.getUserEmail(credential.get('email'))
        if not user.validatePassword(credential.get('password')):
            raise ValueError('Incorrect Password!')
        response = {
            "status": "success",
            "message": "Log in successful",
            getenv("AUTH_HEADER"): auth.createSession(user.id),
            "data": user.toDict(detailed=detailed)
        }
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    return jsonify(response), 200


@app_views.route('/logout', methods=['DELETE'])
@swag_from(f'{DOCS_DIR}/logout.yml')
def logoutUser():
    """Destroys a user session"""
    try:
        token = auth.extractAuthToken(request)
        auth.destroySession(token)
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401

    return jsonify({
        "status": "success",
        "message": "Logout successful"
    })
