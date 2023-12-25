#!/usr/bin/env python3
"""The flask app to serve the graphql"""

from flask import Flask, request, g
from flask_cors import CORS
from os import getenv
from models import storage
from flask_graphql import GraphQLView
from schema import schema
from api.v2.auth import auth


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r'/api/v2/*': {'origins': '*'}}, support_credentials=True)

app.add_url_rule(
    "/api/v2/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True
    )
)

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

if __name__ == "__main__":
    app.run(debug=getenv("DEBUG", False),
            host='0.0.0.0', port=9001, threaded=True)
