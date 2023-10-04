#!/usr/bin/env python3
"""Defines utility classes function for the graphql API"""

import graphene


class UserData(graphene.InputObjectType):
    """Defines a user data class for mutating user object"""
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
