#!/usr/bin/env python3
"""Handles updating user"""

import graphene
from models.user import User as UserModel
from models import storage
from flask import g, abort
from schema.models import User
from models.roles import UserRole
from api.v1.utils.authWrapper import login_required


class UpdateUser(graphene.Mutation):
    """Handles user update"""
    class Arguments:
        """Defines arguments for updating a user"""
        id = graphene.String(required=True)
        updateData = graphene.ObjectType(required=True)

    user = graphene.Field(lambda: User)

    @login_required()
    def mutate(root, info, id, updateData):
        """Creates a new user in the database"""
        updatables = ["username", "email", "password", "firstname", "lastname"]

        if g.currentUser.id != id or g.currentUser.role != UserRole.admin:
            abort(401)
        
        user = storage.get(UserModel, id)
        if not user:
            abort(404)

        for key, value in updateData.items():
            if key in updatables:
                setattr(user, key, value)        

        user.save()

        return UpdateUser(user=user)
