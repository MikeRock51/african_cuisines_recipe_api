#!/usr/bin/env python3
"""Handles updating recipes"""

import graphene
from models.recipe import Recipe as RecipeModel
from models import storage
from flask import g, abort
from schema.models import Recipe
from models.roles import UserRole
from api.v1.utils.authWrapper import login_required
from schema.utils import RecipeData
from sqlalchemy.exc import NoResultFound


class UpdateRecipe(graphene.Mutation):
    """Handles user update"""
    class Arguments:
        """Defines arguments for updating a user"""
        id = graphene.String(required=True)
        updateData = RecipeData(required=True)

    recipe = graphene.Field(lambda: Recipe)

    @login_required()
    def mutate(root, info, id, updateData):
        """Updates a recipe based on ID"""
        nonUpdatables = ['id', 'userID', 'createdAt', 'updatedAt']

        if g.currentUser.id != id and g.currentUser.role not in [
                UserRole.admin, UserRole.moderator, UserRole.editor]:
            abort(401, description="Unauthorized access!")

        try:
            recipe = storage.get(RecipeModel, id)
        except NoResultFound:
            abort(404, description="No recipe found!")

        for key, value in updateData.items():
            if key not in nonUpdatables:
                setattr(recipe, key, value)

        recipe.save()

        return UpdateRecipe(recipe=recipe)
