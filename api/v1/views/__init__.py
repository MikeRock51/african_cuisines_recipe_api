#!/usr/bin/env python3
"""Defines the views module"""

from flask import Blueprint
from models import storage
from flask_graphql import GraphQLView
from schema import schema

graphql_blueprint = Blueprint("graphql", __name__)
graphql_blueprint.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True
    )
)

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/')


from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session import *
from api.v1.views.recipes import *
