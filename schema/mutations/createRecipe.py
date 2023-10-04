#!/usr/bin/env python3
"""Handles recipe creation"""

import graphene
from models.recipe import Recipe as RecipeModel
from models import storage
from flask import g, abort
from api.v1.utils.authWrapper import login_required
from schema.models import Recipe


class CreateRecipe(graphene.Mutation):
    """Creates a recipe"""
    class Arguments:
        """Defines arguments for creating a recipe"""
        name = graphene.String(required=True)
        cuisine = graphene.String(required=False)
        prep_time_minutes = graphene.Int(required=True)
        cook_time_minutes = graphene.Int(required=True)
        serving_size = graphene.Int(required=False)
        calories_per_serving = graphene.Int(required=False)
        ingredients = graphene.List(graphene.String)
        instructions = graphene.List(graphene.String)

    recipe = graphene.Field(lambda: Recipe)

    @login_required()
    def mutate(root, info, name, cuisine, prep_time_minutes,
        cook_time_minutes, ingredients, instructions, serving_size=None,
        calories_per_serving=None):
        """Creates a new recipe in the database"""

        recipe = RecipeModel(
            name = name,
            cuisine = cuisine,
            prep_time_minutes = prep_time_minutes,
            cook_time_minutes = cook_time_minutes,
            userID = g.currentUser.id,
            serving_size = serving_size,
            calories_per_serving = calories_per_serving,
            ingredients = ingredients,
            instructions = instructions
        )

        storage.new(recipe)
        storage.save()

        return CreateRecipe(recipe=recipe)
