#!/usr/bin/env python3
"""Defines utility classes function for the graphql API"""

import graphene


class UserData(graphene.InputObjectType):
    """Defines user data class for mutating user object"""
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()

class RecipeData(graphene.InputObjectType):
    """Defines recipe data for mutating recipe object"""
    name = graphene.String()
    cuisine = graphene.String()
    prep_time_minutes = graphene.Int()
    cook_time_minutes = graphene.Int()
    serving_size = graphene.Int()
    calories_per_serving = graphene.Int()
    ingredients = graphene.List(graphene.String)
    instructions = graphene.List(graphene.String)
