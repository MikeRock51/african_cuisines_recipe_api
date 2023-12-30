#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models.recipeDP import RecipeDP
from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request, g, current_app, make_response, send_from_directory
from api.v2.views import app_views
from api.v2.utils import Utils
from api.v2.utils.authWrapper import login_required
from models.user import User
import re
from flasgger.utils import swag_from
from os import path
from models.ingredients.ingredient import Ingredient
from models.ingredients.ingredientDP import IngredientDP

DOCS_DIR = path.dirname(__file__) + '/documentations/recipes'

@app_views.route('/recipes')
@swag_from(f'{DOCS_DIR}/all_recipes.yml')
def allRecipes():
    """Returns all recipes from database"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    search = " ".join(re.split(r'[-_]', request.args.get('search', '')))
    filterBy = request.args.get('filter_by')
    filterColumns = {}

    if filterBy:
        print(filterBy)
        try:
            filterColumns = Utils.getFilterColumns(filterBy)
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

    data = storage.getPaginatedData(obj=Recipe, page=int(
        page), search=search, filterColumns=filterColumns)

    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


@app_views.route('/recipes/users/<userID>')
@swag_from(f'{DOCS_DIR}/get_user_recipe.yml')
def getUserRecipes(userID):
    """Retrieves all recipes created by a particular user based on userID"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    search = " ".join(re.split(r'[-_]', request.args.get('search', '')))
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
        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

    filterColumns[getattr(Recipe, 'userID')] = [userID]
    data = storage.getPaginatedData(obj=Recipe, page=int(
        page), search=search, filterColumns=filterColumns)

    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


@app_views.route('/recipes/me')
@swag_from(f'{DOCS_DIR}/get_my_recipes.yml')
@login_required()
def getCurrUserRecipes():
    """Retrives all recipes created by the current user"""
    page = request.args.get('page', 1)
    detailed = request.args.get('detailed', False)
    search = " ".join(re.split(r'[-_]', request.args.get('search', '')))
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

    filterColumns[getattr(Recipe, 'userID')] = [g.currentUser.id]

    data = storage.getPaginatedData(obj=Recipe, page=int(
        page), search=search, filterColumns=filterColumns)

    return jsonify(Utils.successResponse(data, detailed, 'recipes')), 200


@app_views.route('/recipes/<id>')
@swag_from(f'{DOCS_DIR}/get_recipe.yml')
def recipeByID(id):
    """Returns a single recipe based on ID"""
    recipe = storage.get(Recipe, id)
    detailed = request.args.get('detailed', False)

    if not recipe:
        abort(404)

    return {
        "status": "success",
        "message": "Recipe retrieved successfully!",
        "data": recipe.toDict(detailed=detailed)
    }


@app_views.route('/recipes', methods=['POST'])
@swag_from(f'{DOCS_DIR}/post_recipes.yml')
@login_required([UserRole.admin, UserRole.moderator, UserRole.editor, UserRole.contributor])
def createRecipe():
    """Creates a new recipe and stores it in database"""
    requiredFields = ['name', 'cuisine', 'ingredients',
                      'instructions', 'nutritional_values', 'prep_time_minutes', 'cook_time_minutes']
    optionalFields = ['total_time_minutes', 'serving_size', 'calories_per_serving']
    objectFields = ['ingredients', 'instructions', 'nutritional_values', 'recipe_dps']

    data = request.form.to_dict()

    Utils.validateRecipeData(data, requiredFields)

    recipeData = {}

    for key, value in data:
        if key in requiredFields or key in optionalFields and key not in objectFields:
            setattr(recipeData, key, value)
    
    recipeData['userID'] = g.currentUser.id
    
    try:
        recipe = Recipe(**recipeData)
        recipe.save()
        
        requiredFields = ['name']
        optionalFields = ['description', 'quantity']

        if "recipe_dps" in data:
            DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/recipes/{recipe.id}'
            recipe_dps = data['recipe_dps']
            dpFiles = request.files.getlist('recipe_dps[]')
            dpData = {
                "recipeID": recipe.id,
                "userID": g.currentUser.id
            }
            Utils.processDPFiles(recipe_dps, dpFiles, RecipeDP, DP_FOLDER, dpData)

        for ingr in data['ingredients']:
            if "name" not in ingr:
                abort(400, description="Missing required field: name")
            for field in ingr:
                if field not in requiredFields and field not in optionalFields:
                    ingr.pop(field)
            ingredient = Ingredient(**ingr)
            
            if "ingredient_dps" in ingr:
                DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/ingredients/{ingredient.id}'
                ingredient_dps = ingr['ingredients_dps']
                dpFiles = request.files.getlist('ingredient_dps[]')
                dpData = { "ingredientID": ingredient.id }
                Utils.processDPFiles(ingredient_dps, dpFiles, IngredientDP, DP_FOLDER, dpData)

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
@swag_from(f'{DOCS_DIR}/put_recipes.yml')
@login_required()
def updateRecipe(id):
    """Updates the recipe with the id"""
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404, description="Recipe not found!")

    nonUpdatables = ['id', 'userID', 'createdAt', 'updatedAt']
    privilegedRoles = [UserRole.admin, UserRole.moderator, UserRole.editor]

    if g.currentUser.id != recipe.userID and g.currentUser.role not in privilegedRoles:
        abort(401, description="You are not authorized to update this recipe")

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
@swag_from(f'{DOCS_DIR}/delete_recipes.yml')
@login_required()
def deleteRecipe(id):
    """Deletes the recipe with the id"""
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404, description="Recipe not found!")

    privilegedRoles = [UserRole.admin, UserRole.moderator]
    if g.currentUser.id != recipe.userID and g.currentUser.role not in privilegedRoles:
        abort(401, description="You are not authorized to delete this recipe!")

    storage.delete(recipe)

    return jsonify({
        "status": "success",
        "message": "Recipe deleted successfully!",
        "data": None
    }), 200
