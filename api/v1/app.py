#!/usr/bin/env python3
"""The flask app"""

from flask import Flask, jsonify, request, abort, g
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from api.v1.auth import auth


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r'/api/v1/*': {'origins': '*'}}, support_credentials=True)


@app.before_request
def preRequest():
    """Handles prequest setups and validations"""
    try:
        token = auth.extractAuthToken(request)
        userID = auth.getSession(token)
        g.currentUser = auth.getUserID(userID)
    except ValueError:
        g.currentUser = None

@app.errorhandler(400)
def badRequest(error):
    """Handles 400 errors"""
    return jsonify({
        "status": "error",
        "message": "Bad request"
    })

@app.errorhandler(401)
def unauthorized(error):
    """Handles 401 errors"""
    return jsonify({
        "status": "error",
        "message": "Unauthorized"
    })

@app.errorhandler(403)
def forbidden(error):
    """Handles 403 errors"""
    return jsonify({
        "status": "error",
        "message": "Forbidden"
    })

@app.errorhandler(404)
def notFound(error):
    """Handles 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Not found!!!"
    })


if __name__ == "__main__":
   app.run(debug=getenv("DEBUG", False), host='0.0.0.0', port=6000, threaded=True)
