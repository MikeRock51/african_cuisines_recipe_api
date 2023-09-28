#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.utils.authWrapper import login_required


@app_views.route('/recipes')
def allRecipes():
    """Returns all recipes from database"""
    page = request.args.get('page')
    detailed = request.args.get('detailed', False)
    filter_by = request.args.get('filter_by')
    filter_columns = {}

    if filter_by:
        columns = filter_by.split('/')
        for column in columns:
            key, value = column.split()
            try:
                filter_columns[key] = int(value)
            except ValueError:
                filter_columns[key] = value

    print(filter_columns)

    return jsonify({})
