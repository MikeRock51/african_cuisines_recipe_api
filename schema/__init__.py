#!/usr/bin/env python3
"""Defines the GraphQL schema for the api"""

import collections.abc
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.recipe import Recipe as RecipeModel
from models.user import User as UserModel
from models import storage
from flask import g
from api.v1.utils.authWrapper import login_required
from models.roles import UserRole


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

class Query(graphene.ObjectType):
    """Defines the entry point for querying data from the API"""
    node = graphene.relay.Node.Field()
    recipes = SQLAlchemyConnectionField(Recipe.connection)
    users = SQLAlchemyConnectionField(User.connection)
    user = graphene.Field(User)

    @login_required()
    def resolve_users(self, info, sort=None):
        """Handles queries for users"""
        return self

class CreateUser(graphene.Mutation):
    """Handles user creation"""
    class Arguments:
        """Defines arguments for creating a user"""
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        firstname = graphene.String(required=False)
        lastname = graphene.String(required=False)

    user = graphene.Field(lambda: User)

    def mutate(root, info, username, email, password, firstname="", lastname=""):
        """Creates a new user in the database"""
        user = UserModel(
            username=username,
            email=email,
            _password=password,
            firstname=firstname,
            lastname=lastname
        )

        storage.new(user)
        storage.save()

        return CreateUser(user=user)
    
class Mutations(graphene.ObjectType):
    """Handles all POST/PUT actions"""
    createUser = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
