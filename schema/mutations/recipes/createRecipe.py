#!/usr/bin/env python3
"""Handles recipe creation"""

import graphene
from models.recipe import Recipe as RecipeModel
from models import storage
from flask import g, abort
from api.v1.utils.authWrapper import login_required
from schema.models import Recipe
from schema.utils import RecipeData


class CreateRecipe(graphene.Mutation):
    """Creates a recipe"""
    class Arguments:
        """Defines arguments for creating a recipe"""
        recipeData = RecipeData(required=True)

    recipe = graphene.Field(lambda: Recipe)

    @login_required()
    def mutate(root, info, recipeData):
        """Creates a new recipe in the database"""
        recipeData['userID'] = g.currentUser.id
        recipe = RecipeModel(**recipeData)
        recipe.save()

        return CreateRecipe(recipe=recipe)
