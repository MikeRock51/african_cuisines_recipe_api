#!/usr/bin/env python3
"""Defines the GraphQL schema for the api"""

from graphene import relay, ObjectType, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.recipe import Recipe as RecipeModel


class Recipe(SQLAlchemyObjectType):
    """Defines a GraphQL type for a user"""
    class Meta:
        """Defines metadata and configuration for a user"""
        model = RecipeModel
        interfaces = (relay.Node,)

class Query(ObjectType):
    """Defines the entry point for querying data from the API"""
    node = relay.Node.Field()
    recipes = SQLAlchemyConnectionField(Recipe.connection)

schema = Schema(query=Query)
