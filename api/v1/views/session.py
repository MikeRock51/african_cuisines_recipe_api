#!/usr/bin/env python3
"""Handles user session"""

from flask import request, jsonify
from api.v1.views import app_views
from api.v1.auth import auth
from api.v1.utils.utilities import Utilities
from models import storage
from models.user import User
from dotenv import load_dotenv
from os import getenv

load_dotenv()


@app_views.route('/login', methods=['POST'])
def userLogin():
    """Creates a user session"""
    requiredFields = ['email', 'password']
    try:
        credential = Utilities.getReqJSON(request, requiredFields)
        user = auth.getUser(credential.get('email'))
        if not user.validatePassword(credential.get('password')):
            raise ValueError('Incorrect Password!')
        response = {
                "status": "success",
                "message": "Log in successful",
                getenv("AUTH_HEADER"): auth.createSession(user.id)
        }
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
    return jsonify(response), 200


@app_views.route('/logout')
def logoutUser():
    """Destroys a user session"""
    try:
        token = auth.extractAuthToken(request)
        auth.destroySession(token)
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

    return jsonify({
        "status": "success",
        "message": "Logout successful"
    })
