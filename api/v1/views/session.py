#!/usr/bin/env python3
"""Handles user session"""

from flask import request, jsonify
from api.v1.views import app_views
from api.v1.auth import auth
from api.v1.utils.utilities import Utilities
from models import storage
from models.user import User

@app_views.route('/login', methods=['POST'])
def userLogin():
    """Handles user log in"""
    requiredFields = ['email', 'password']
    try:
        credential = Utilities.getReqJSON(request, requiredFields)
        user = auth.getUser(credential.get('email'))
        if not user.validatePassword(credential.get('password')):
            raise ValueError('Incorrect Password!')
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
    return jsonify(credential)
