#!/usr/bin/env python3
"""Handles user creation"""

import graphene
from models.user import User as UserModel
from models import storage
from flask import g
from schema.models import User
from schema.utils import UserData


class CreateUser(graphene.Mutation):
    """Handles user creation"""
    class Arguments:
        """Defines arguments for creating a user"""
        userData = UserData(required=True)

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
