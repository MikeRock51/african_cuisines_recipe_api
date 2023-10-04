#!/usr/bin/env python3
"""Handles user creation"""

import graphene
from models.user import User as UserModel
from models import storage
from flask import g, abort
from schema.models import User
from schema.utils import UserData


class CreateUser(graphene.Mutation):
    """Handles user creation"""
    class Arguments:
        """Defines arguments for creating a user"""
        userData = UserData(required=True)

    user = graphene.Field(lambda: User)

    def mutate(root, info, userData):
        """Creates a new user in the database"""
        requiredFields = ["username", "email", "password"]

        for attr in requiredFields:
            if attr not in userData:
                error = f"Please include {attr} in your request"
                abort(400, description=error)

        username = userData['username']
        userData['username'] = "_".join(username.split())
        user = UserModel(**userData)
        user.save()

        return CreateUser(user=user)
