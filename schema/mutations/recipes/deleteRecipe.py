#!/usr/bin/env python3
"""Handles deleting recipe"""

import graphene
from models.recipe import Recipe as RecipeModel
from models import storage
from flask import g, abort
from schema.models import Recipe
from models.roles import UserRole
from api.v1.utils.authWrapper import login_required
from sqlalchemy.exc import NoResultFound


class DeleteRecipe(graphene.Mutation):
    """Handles recipe delete"""
    class Arguments:
        """Defines arguments for deleting a recipe"""
        id = graphene.String(required=True)

    recipe = graphene.Field(lambda: Recipe)

    @login_required()
    def mutate(root, info, id):
        """Deletes a recipe from database"""
        try:
            recipe = storage.get(RecipeModel, id)
        except NoResultFound:
            abort(404, description="No recipe found!")

        if g.currentUser.id != recipe.userID and g.currentUser.role\
                not in [UserRole.admin, UserRole.moderator]:
            abort(401, description="Unauthorized to delete this recipe!")

        recipe.delete()

        return DeleteRecipe()
