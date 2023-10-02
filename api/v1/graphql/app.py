#!/usr/bin/env python3
"""The flask app to serve the graphql"""

from flask import Flask
from flask_cors import CORS
from os import getenv
from models import storage
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r'/api/v1/*': {'origins': '*'}}, support_credentials=True)

app.add_url_rule(
    "/api/v1/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True
    )
)

@app.teardown_appcontext
def tearDown(self):
    """Removes the current database session after each request"""
    storage.close()

if __name__ == "__main__":
    app.run(debug=getenv("DEBUG", False),
            host='0.0.0.0', port=9001, threaded=True)
