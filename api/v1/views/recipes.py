#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.utils import Utils
from api.v1.utils.authWrapper import login_required
import re


@app_views.route('/recipes')
def allRecipes():
    """Returns all recipes from database"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    keyword = " ".join(re.split(r'[-_]', request.args.get('keyword', '')))
    filterBy = request.args.get('filter_by')
    filterColumns = {}

    if filterBy:
        columns = filterBy.split(':')
        for column in columns:
            key, value = column.split()
            try:
                filterColumns[getattr(Recipe, key)] = int(value)
            except ValueError:
                filterColumns[getattr(Recipe, key)] = [" ".join(re.split(r'[_-]', col)) for col in value.split(',')]
    
    data = storage.getPaginatedData(obj=Recipe, page=int(page), keyword=keyword, filterColumns=filterColumns)

    return jsonify({
        "status": "success",
        "message": "Sucessfully fetched recipes" if data['data'] != [] else "No match found",
        "data": [recipe.toDict(detailed=detailed) for recipe in data['data']],
        "page": data['page'],
        "page_size": data['page_size'],
        "total_page_items": data['total_items'],
        "total_pages": data['total_pages']
    })

@app_views.route('/recipes/<id>')
def recipeByID(id):
    """Returns a single recipe based on ID"""
    recipe = storage.get(Recipe, id)
    detailed = request.args.get('detailed', False)

    if not recipe:
        abort(404)

    return recipe.toDict(detailed=detailed)

@app_views.route('/recipes', methods=['POST'])
@login_required([UserRole.admin, UserRole.moderator, UserRole.editor, UserRole.contributor])
def createRecipe():
    """Creates a new recipe and stores it in database"""
    requiredFields = ['name', 'userID', 'cuisine', 'ingredients', 'instructions', 'prep_time_minutes', 'cook_time_minutes']
    optionalFields = ['total_time_minutes', 'serving_size', 'calories_per_serving']
    try:
        recipeData = Utils.getReqJSON(request, requiredFields)
        for field in recipeData:
            if field not in requiredFields and field not in optionalFields:
                recipeData.pop(field)
        recipe = Recipe(**recipeData)
        recipe.save()
    except (ValueError) as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        }), 400

    return jsonify({
        "status": "error",
        "message": "Recipe created successfully",
        "data": recipe.toDict(detailed=True)
    })
