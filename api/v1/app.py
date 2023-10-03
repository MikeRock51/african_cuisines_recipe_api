#!/usr/bin/env python3
"""The flask app"""

from flask import Flask, jsonify, request, abort, g
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from api.v1.auth import auth
from models import storage
from flasgger import Swagger
# from flask_graphql import GraphQLView
# from schema import Recipe, schema


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.sort_keys = False
CORS(app, resources={r'/api/v1/*': {'origins': '*'}}, support_credentials=True)

app.register_blueprint(app_views)

@app.before_request
def authenticate():
    """Handles pre request setups and validations"""
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
        "message": "Bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handles 401 errors"""
    return jsonify({
        "status": "error",
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """Handles 403 errors"""
    return jsonify({
        "status": "error",
        "message": "Forbidden"
    }), 403


@app.errorhandler(404)
def notFound(error):
    """Handles 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Not Found"
    }), 404


app.config['SWAGGER'] = {
    'title': 'African Cuisines Recipe Restful API',
    'description': 'A RESTFUL API that provides detailed information about African cuisines. As well as step by step instructions on how to make them.',
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
    'schemes': ["http", "https"],
    'specs_route': '/api/v1/docs',
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
