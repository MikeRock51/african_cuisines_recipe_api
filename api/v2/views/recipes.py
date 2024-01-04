#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models.recipeDP import RecipeDP
from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request, g, current_app, make_response, send_from_directory
from api.v2.views import app_views
from api.v2.utils import Utils, VError
from api.v2.utils.authWrapper import login_required
from models.user import User
import re
from flasgger.utils import swag_from
from os import path
from models.ingredients.ingredient import Ingredient
from models.ingredients.ingredientDP import IngredientDP
from models.instructions.instruction import Instruction
from models.instructions.instructionMedia import InstructionMedia
from models.nutritions.nutritionalValue import NutritionalValue
from models.nutritions.nutritionDP import NutritionDP
from models.instructions.videoInstruction import VideoInstruction
import json

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

    # print(type(json.loads(data['recipe_dps'])))

    Utils.validateRecipeData(data, requiredFields)

    recipeData = {}

    for key, value in data.items():
        if key not in objectFields and key in requiredFields or key in optionalFields:
            recipeData[key] = value
    
    recipeData['userID'] = g.currentUser.id

    try:
        recipe = Recipe(**recipeData)
        recipe.save()
        
        if "recipe_dps" in data:
            DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/recipes/{recipe.id}'
            recipe_dps = json.loads(data['recipe_dps'])
            required = ['fileType']
            dpFiles = request.files.getlist('recipe_dps[]')
            dpData = {
                "recipeID": recipe.id,
                "userID": g.currentUser.id
            }
            Utils.processFiles(recipe_dps, dpFiles, RecipeDP, DP_FOLDER, dpData, required)
        
        ingredients = json.loads(data['ingredients'])
        requiredFields = ['name']
        optionalFields = ['description', 'quantity', 'quantity_metric']
        for ingr in ingredients:
            for field in requiredFields:
                if field not in ingr:
                    raise VError(f"Missing required ingredient field {field}", 400)
                    # abort(400, description=f"Missing required field: {field}")
            ingredientFields = {}
            for field in ingr:
                if field in requiredFields or field in optionalFields:
                    ingredientFields[field] = ingr[field]
            ingredientFields['recipeID'] = recipe.id
            ingredient = Ingredient(**ingredientFields)
            ingredient.save()
            
            if "ingredient_dps" in ingr:
                DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/ingredients/{ingredient.id}'
                print(type(ingr['ingredient_dps']))
                # ingredient_dps = json.loads(ingr['ingredient_dps'])
                required = ['fileType']
                dpFiles = request.files.getlist('ingredient_dps[]')
                dpData = { "ingredientID": ingredient.id }
                Utils.processFiles(ingr['ingredient_dps'], dpFiles, IngredientDP, DP_FOLDER, dpData, required)

        requiredFields = ['title']
        optionalFields = ['description']
        instructions = json.loads(data['instructions'])
        for instruct in instructions:
            for field in requiredFields:
                if field not in instruct:
                    raise VError(f"Missing required instruction field {field}", 400)
                    # abort(400, description=f"Missing required field: {field}")
            instructionFields = {}
            for field in instruct:
                if field in requiredFields or field in optionalFields:
                    instructionFields[field] = instruct[field]
            instructionFields['recipeID'] = recipe.id
            instruction = Instruction(**instructionFields)
            instruction.save()
            
            if "instruction_medias" in instruct:
                DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/instructions/{instruction.id}'
                # instruction_medias = json.loads(instruct['instruction_medias'])
                # print(f'Instruction Medias: {instruction_medias}')
                required = ['fileType', 'format']
                mediaFiles = request.files.getlist('instruction_medias[]')
                # print(f'Media Files: {mediaFiles}')
                dpData = { "instructionID": instruction.id }
                Utils.processFiles(instruct['instruction_medias'], mediaFiles, InstructionMedia, DP_FOLDER, dpData, required)

        requiredFields = ['title']
        optionalFields = ['description']
        nutritional_values = json.loads(data['nutritional_values'])
        for value in nutritional_values:
            for field in requiredFields:
                if field not in value:
                    raise VError(f"Missing required nutritional_value field: {field}", 400)
            nutritionFields = {}
            for field in value:
                if field in requiredFields or field in optionalFields:
                    nutritionFields[field] = value[field]
            nutritionFields['recipeID'] = recipe.id
            nutritional_value = NutritionalValue(**nutritionFields)
            nutritional_value.save()
            
            if "nutrition_dps" in value:
                DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/nutritional_values/{nutritional_value.id}'
                # nutrition_dps = json.loads(value['nutrition_dps'])
                required = ['fileType']
                dpFiles = request.files.getlist('nutrition_dps[]')
                dpData = { "nutritionID": nutritional_value.id }
                Utils.processFiles(value['nutrition_dps'], dpFiles, NutritionDP, DP_FOLDER, dpData, required)

        if "video_instruction" in data:
            instructionVid = json.loads(data['video_instruction'])
            requiredFields = ['title', 'fileType']
            optionalFields = ['description']

            for field in requiredFields:
                if field not in instructionVid:
                    raise VError(f"Missing required video_instruction field: {field}", 400)
            vidFields = {}
            for field in instructionVid:
                if field in requiredFields or field in optionalFields:
                    vidFields[field] = instructionVid[field]
            vidFields['recipeID'] = recipe.id
            if vidFields['fileType'].lower() == 'link':
                if 'filePath' not in instructionVid:
                    raise VError("Missing required video_instruction field: filePath", 400)
                vidFields['filePath'] = instructionVid['filePath']
            elif vidFields['fileType'].lower() == 'file':
                UPLOAD_FOLDER = f'{current_app.config["VIDEO_FOLDER"]}/video_instructions/{instructionVid.id}'
                videoFile = request.files.getlist('instruction_video')[0]
                filename = Utils.uploadSingleFile(videoFile, UPLOAD_FOLDER, current_app.config['ALLOWED_VIDEOS'])
                vidFields['filePath'] = filename
            video_instruction = VideoInstruction(**vidFields)
            video_instruction.save()
    except (VError) as ve:
        if recipe:
            storage.delete(recipe)
        return jsonify({
            "status": "error",
            "message": str(ve),
            "data": None
        }), ve.statusCode
    # except (Exception) as e:
    #     if recipe:
    #         storage.delete(recipe)
    #     return jsonify({
    #         "status": "error",
    #         "message": str(e),
    #         "data": None
    #     }), 400

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
