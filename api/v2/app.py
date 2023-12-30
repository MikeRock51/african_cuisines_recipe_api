#!/usr/bin/env python3
"""The flask app"""

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from api.v2.views import app_views
from os import getenv, path
from api.v2.auth import auth
from models import storage
from flasgger import Swagger


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['DP_FOLDER'] = path.dirname(__file__) + '/assets/dps'
app.config['ALLOWED_IMAGES'] = {'png', 'jpg', 'jpeg', 'gif'}
app.json.sort_keys = False
CORS(app, resources={r'/api/v2/*': {'origins': '*'}}, support_credentials=True)
app.register_blueprint(app_views)

@app.before_request
def authenticate():
    """Handles pre-request setups and validations"""
    try:
        token = auth.extractAuthToken(request)
        userID = auth.getSession(token)
        g.currentUser = auth.getUserID(userID)
    except ValueError:
        g.currentUser = None

@app.teardown_appcontext
def tearDown(self):
    """Removes the current database session after each request"""
    storage.close()

@app.errorhandler(400)
def badRequest(error):
    """Handles 400 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Bad request",
        "data:": None
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    """Handles 401 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Unauthorized",
        "data:": None
    }), 401

@app.errorhandler(403)
def forbidden(error):
    """Handles 403 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Forbidden",
        "data:": None
    }), 403

@app.errorhandler(404)
def notFound(error):
    """Handles 404 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Not Found",
        "data:": None
    }), 404

@app.errorhandler(409)
def unauthorized(error):
    """Handles 409 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Conflicting resources",
        "data:": None
    }), 409

@app.errorhandler(406)
def unauthorized(error):
    """Handles 406 errors"""
    return jsonify({
        "status": "error",
        "message": error.description or "Resource unacceptable!",
        "data:": None
    }), 409

app.config['SWAGGER'] = {
    'title': 'African Cuisines Recipe Restful API',
    'description': 'A RESTFUL API that provides detailed information about African cuisines. As well as step by step instructions on how to make them. It also features a chat route, where you can interact with Yishu, a health and nutrition chatbot',
    'uiversion': 3,
    'version': '1.0.0',
    'securityDefinitions': {
        "Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "auth-token"
        }
    },
    'security': [{'ApiKeyAuth': []}],
    # 'schemes': ["https", "http"],
    'specs_route': '/api/v2/docs',
    "security": [{"ApiKeyAuth": []}],
    "displayOperationId": True,
    "displayRequestDuration": True,
    "hide_top_bar": True
}
# app.register_blueprint(graphql_blueprint)
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=getenv("DEBUG", False),
            host='0.0.0.0', port=9000, threaded=True)
