#!/usr/bin/env python3
"""Index views"""

from api.v2.views import app_views
from flask import jsonify, request
from flasgger import swag_from


@app_views.route('/status')
def getStatus():
    """
    Returns the status of the server
    responses:
      200:
        description: All systems green!
    """
    return jsonify({
        "status": "success",
        "message": "All systems green!"
    })

@app_views.route('/test', methods=['POST'])
def testBody():
    """
    Returns the status of the server
    responses:
      200:
        description: All systems green!
    """
    body = request.get_json()
    
    if "name" not in body:
        return jsonify({"error": "No Name"}), 400

    name = body['name']
    
    return jsonify({
        "status": "success",
        "message": "All systems green!",
        "data": name
    })
