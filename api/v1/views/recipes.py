#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request, g
from api.v1.views import app_views
from api.v1.utils import Utils
from api.v1.utils.authWrapper import login_required
from models.user import User
import re
from flasgger.utils import swag_from


@app_views.route('/recipes')
def allRecipes():
    """Returns all recipes from database"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    keyword = " ".join(re.split(r'[-_]', request.args.get('keyword', '')))
    filterBy = request.args.get('filter_by')
    filterColumns = {}

    if filterBy:
        try:
            filterColumns = Utils.getFilterColumns(filterBy)
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

    data = storage.getPaginatedData(obj=Recipe, page=int(
                page), keyword=keyword, filterColumns=filterColumns)
    
    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


@app_views.route('/recipes/<userID>')
def getUserRecipes(userID):
    """Retrives all recipes created by a particular user based on userID"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    keyword = " ".join(re.split(r'[-_]', request.args.get('keyword', '')))
    filterBy = request.args.get('filter_by')
    filterColumns = {}
    user = storage.get(User, userID)

    if not user:
        return jsonify({
            "status": "error",
            "message": "This user does not exist"
        }), 404

    if filterBy:
        try:
            filterColumns = Utils.getFilterColumns(filterBy)
            filterColumns[getattr(Recipe, 'userID')] = [userID]
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

    data = storage.getPaginatedData(obj=Recipe, page=int(
        page), keyword=keyword, filterColumns=filterColumns)

    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


@app_views.route('/recipes/me')
@login_required()
def getCurrUserRecipes():
    """Retrives all recipes created by the current user"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    keyword = " ".join(re.split(r'[-_]', request.args.get('keyword', '')))
    filterBy = request.args.get('filter_by')

    if filterBy:
        try:
            filterColumns = Utils.getFilterColumns(filterBy)
            filterColumns[getattr(Recipe, 'userID')] = [g.currentUser.id]

            data = storage.getPaginatedData(obj=Recipe, page=int(
                page), keyword=keyword, filterColumns=filterColumns)
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


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
    requiredFields = ['name', 'cuisine', 'ingredients',
                      'instructions', 'prep_time_minutes', 'cook_time_minutes']
    optionalFields = ['total_time_minutes',
                      'serving_size', 'calories_per_serving']
    try:
        recipeData = Utils.getReqJSON(request, requiredFields)
        for field in recipeData:
            if field not in requiredFields and field not in optionalFields:
                recipeData.pop(field)
        recipeData['userID'] = g.currentUser.id
        recipe = Recipe(**recipeData)
        recipe.save()
    except (ValueError) as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        }), 400

    data = recipe.toDict(detailed=True)
    return jsonify({
        "status": "success",
        "message": "Recipe created successfully",
        "data": data
    })


@app_views.route('/recipes/<id>', methods=['PUT'])
@login_required()
def updateRecipe(id):
    """Updates the recipe with the id"""
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404)

    nonUpdatables = ['id', 'userID', 'createdAt', 'updatedAt']
    privilegedRoles = [UserRole.admin, UserRole.moderator, UserRole.editor]

    if g.currentUser.id != recipe.userID and g.currentUser.role not in privilegedRoles:
        abort(401)

    try:
        data = Utils.getReqJSON(request)
        for key, value in data.items():
            if key not in nonUpdatables and hasattr(Recipe, key):
                setattr(recipe, key, value)
        recipe.save()
    except (ValueError, Exception) as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        }), 400

    return jsonify({
        "status": "success",
        "message": "Recipe updated successfully!",
        "data": recipe.toDict(detailed=True)
    })


@app_views.route('/recipes/<id>', methods=['DELETE'])
@login_required()
def deleteRecipe(id):
    """Deletes the recipe with the id"""
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404)

    privilegedRoles = [UserRole.admin, UserRole.moderator]
    if g.currentUser.id != recipe.userID and g.currentUser.role not in privilegedRoles:
        abort(401)

    storage.delete(recipe)

    return jsonify({
        "status": "success",
        "message": "Recipe deleted successfully!"
    }), 200
