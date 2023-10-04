#!/usr/bin/env python3
"""Handles deleting user"""

import graphene
from models.user import User as UserModel
from models import storage
from flask import g, abort
from schema.models import User
from models.roles import UserRole
from api.v1.utils.authWrapper import login_required
from sqlalchemy.exc import NoResultFound


class DeleteUser(graphene.Mutation):
    """Handles user delete"""
    class Arguments:
        """Defines arguments for deleting a user"""
        id = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    @login_required()
    def mutate(root, info, id):
        """Deletes a user from database"""
        try:
            user = storage.get(UserModel, id)
        except NoResultFound:
            abort(404, description="No user found!")

        if g.currentUser.id != id and g.currentUser.role != UserRole.admin:
            abort(401, description="Unauthorized access!")

        user.delete()

        return DeleteUser()
