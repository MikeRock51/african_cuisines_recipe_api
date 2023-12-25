#!/usr/bin/env python3
"""Defines the views module"""

from flask import Blueprint
# from models import storage
# from flask_graphql import GraphQLView
# from schema import schema

# graphql_blueprint = Blueprint("graphql", __name__)
# graphql_blueprint.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view(
#         "graphql",
#         schema=schema,
#         graphiql=True
#     )
# )

app_views = Blueprint('app_views', __name__, url_prefix='/api/v2/')


from api.v2.views.index import *
from api.v2.views.users import *
from api.v2.views.session import *
from api.v2.views.recipes import *
from api.v2.views.chats import *
from api.v2.views.dps import *
