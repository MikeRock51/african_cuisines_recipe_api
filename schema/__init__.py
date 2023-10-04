#!/usr/bin/env python3
"""Defines the GraphQL schema for the api"""

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from models.recipe import Recipe as RecipeModel
from models.user import User as UserModel
from models import storage
from schema.models import User, Recipe
from flask import g, abort
from api.v1.utils.authWrapper import login_required
from models.roles import UserRole
from schema.mutations.users.createUser import CreateUser
from schema.mutations.users.updateUser import UpdateUser
from schema.mutations.users.deleteUser import DeleteUser
from schema.mutations.recipes.createRecipe import CreateRecipe
from schema.mutations.recipes.updateRecipe import UpdateRecipe


class Query(graphene.ObjectType):
    """Defines the entry point for querying data from the API"""
    node = graphene.relay.Node.Field()

    recipes = SQLAlchemyConnectionField(
        Recipe.connection, page=graphene.Int(), search=graphene.String())
    recipe = graphene.Field(Recipe, id=graphene.String())

    users = SQLAlchemyConnectionField(User.connection)
    user = graphene.Field(User, id=graphene.String())

    def resolve_recipes(self, info, sort=None, page=1, search=""):
        """Handles recipe fetching and paginating recipes"""
        recipes = storage.getPaginatedData(obj=RecipeModel, search=search, page=page)
        recipes = recipes['data']
        for recipe in recipes:
            if recipe.author._password:
                del recipe.author._password

        return recipes

    def resolve_recipe(self, info, id):
        """Fetches a recipe based on ID"""
        # recipe = RecipeModel.query.filter(RecipeModel.id == id).one()
        recipe = storage.get(RecipeModel, id)
        if not recipe:
            abort(404, description="Recipe not found!")

        del recipe.author._password
        return recipe

    @login_required()
    def resolve_user(self, info, id):
        """Fetches a user based on ID"""
        user = UserModel.query.filter(UserModel.id == id).one()
        del user._password

        if user.id == g.currentUser.id or g.currentUser.role == UserRole.admin:
            return user
        else:
            abort(401, description="Unauthorized access!")

    @login_required([UserRole.admin])
    def resolve_users(self, info, sort=None):
        """Handles queries for users"""
        return self

class Mutations(graphene.ObjectType):
    """Handles all POST/PUT actions"""
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    createRecipe = CreateRecipe.Field()
    updateRecipe = UpdateRecipe.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
