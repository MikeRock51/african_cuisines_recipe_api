#!/usr/bin/env python3
"""Defines the GraphQL schema for the api"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.recipe import Recipe as RecipeModel
from models.user import User as UserModel


class Recipe(SQLAlchemyObjectType):
    """Defines a GraphQL type for a Recipe"""
    class Meta:
        """Defines metadata and configuration for a recipe"""
        model = RecipeModel
        interfaces = (graphene.relay.Node,)


class User(SQLAlchemyObjectType):
    """Defines a GraphQL type for a User"""
    class Meta:
        """Defines metadata and configuration for a user"""
        model = UserModel
        interfaces = (graphene.relay.Node,)
