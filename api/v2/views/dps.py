#!/usr/bin/env python3
"""RESTFUL API actions for recipes"""

from models.recipe import Recipe
from models.recipeDP import RecipeDP
from models.user import User
from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request, g, current_app, make_response, send_from_directory
from api.v2.views import app_views
from api.v2.utils import Utils
from api.v2.utils.authWrapper import login_required
from flasgger.utils import swag_from
from os import path
from sqlalchemy.exc import IntegrityError

DOCS_DIR = path.dirname(__file__) + '/documentations'


@app_views.route('/recipes/dps', methods=['PUT'])
@swag_from(f'{DOCS_DIR}/recipes/put_recipe_dp.yml')
@login_required()
def uploadRDP():
    """Uploads a recipe's display picture"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    fileData = request.form.to_dict()
    requiredFields = ['fileType', 'recipeID']
    dp = None

    for field in requiredFields:
        if field not in fileData:
            abort(400, description=f"Missing required field: {field}")

    recipe = storage.get(Recipe, fileData['recipeID'])

    if not recipe:
        abort(404, description="Recipe not found!")

    try:
        if fileData['fileType'] == 'link':
            if 'filePath' not in fileData:
                abort(400, description="Missing required field: filePath")

            for dp in recipe.dps:
                if dp.filePath == fileData['filePath']:
                    abort(409, description="This dp already exist")

            dp = RecipeDP(
                filePath=fileData['filePath'], recipeID=fileData['recipeID'], userID=g.currentUser.id)
            dp.save()
        else:
            DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/recipes/{fileData["recipeID"]}'

            if 'file' not in request.files:
                abort(400, description="File is missing")

            filename = Utils.uploadFile(
                request, DP_FOLDER, ALLOWED_EXTENSIONS)

            for dp in recipe.dps:
                if dp.filePath == filename:
                    abort(409, description="This dp already exist")

            dp = RecipeDP(filePath=filename,
                          recipeID=fileData['recipeID'], fileType="file", userID=g.currentUser.id)
            dp.save()
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve),
            "data": None
        }), 400
    except IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(ie)),
            "data": None
        }), 400

    return jsonify({
        "status": "success",
        "message": "Recipe image uploaded successfully!",
        "data": dp.toDict()
    }), 201


@app_views.route('/recipes/dps/<dpID>', methods=['GET'])
@swag_from(f'{DOCS_DIR}/recipes/get_recipe_dp.yml')
def getDP(dpID):
    """Retrieves a recipe dp file based on ID"""
    response = None

    try:
        dp = storage.get(RecipeDP, dpID)
        if not dp:
            abort(404, description="DP not found!")

        if dp.fileType != 'file':
            abort(406, description="Only dps with fileType: file is acceptable!")

        DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/recipes/{dp.recipeID}'
        response = make_response(send_from_directory(DP_FOLDER, dp.filePath))
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve),
            "data": None
        }), 400
    except IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(ie)),
            "data": None
        }), 400

    return response

@app_views.route('/recipes/<recipeID>/dps', methods=['GET'])
@swag_from(f'{DOCS_DIR}/recipes/get_recipe_dps.yml')
def getrecipeDPs(recipeID):
    """Retrieves all dp objects asociated with a recipe"""
    dps = storage.getByItemID(RecipeDP, "recipeID", recipeID)
    
    return jsonify({
        "status": "success",
        "message": "Recipe dps retrieved successfully!",
        "data": [dp.toDict() for dp in dps]
    }), 200

@app_views.route('/recipes/dps/<dpID>', methods=['DELETE'])
@swag_from(f'{DOCS_DIR}/recipes/delete_recipe_dp.yml')
@login_required()
def deleteDP(dpID):
    """Deletes a recipe dp based on ID"""
    privilegedRoles = [UserRole.admin, UserRole.moderator]
    
    try:
        dp = storage.get(RecipeDP, dpID)
        if not dp:
            abort(404, description="DP not found!")

        if dp.userID != g.currentUser.id and g.currentUser.role not in privilegedRoles:
            abort(401, description="You are not authorized to delete this dp!")

        if dp.fileType == 'file':
            DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/recipes/{dp.recipeID}'
            Utils.deleteFile(f'{DP_FOLDER}/{dp.filePath}')

        storage.delete(dp)
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve),
            "data": None
        }), 400
    except IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(ie)),
            "data": None
        }), 400

    return jsonify({
        "status": "success",
        "message": "DP deleted successfully!",
        "data": None
    }), 204

@app_views.route('/users/dp', methods=['PUT'])
@swag_from(f'{DOCS_DIR}/users/put_user_dp.yml')
@login_required()
def uploadDP():
    """Uploads and updates a user's Display Picture"""
    DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/users/{g.currentUser.id}'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    try:
        if 'file' not in request.files:
            abort(400, description="File is missing")

        filename = Utils.uploadFile(
            request, DP_FOLDER, ALLOWED_EXTENSIONS)
        
        Utils.deleteFile(f'{DP_FOLDER}/{g.currentUser.dp}')
        g.currentUser.dp = filename
        g.currentUser.save()
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(ie))
        }), 400

    return jsonify({
        "status": "success",
        "message": "User DP uploaded successfully",
        "data": g.currentUser.toDict()
    }), 201


@app_views.route('/users/dp/<userID>', methods=['GET'])
@swag_from(f'{DOCS_DIR}/users/get_user_dp.yml')
# @login_required()
def getUserDP(userID):
    """Retrieves the current users display picture file"""
    user = storage.get(User, userID)
    if not user:
        abort(404, description="No user with this ID")

    DP_FOLDER = ""
    if user.dp == 'defaultDP.png':
        DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/users'
    else:
        DP_FOLDER = f'{current_app.config["DP_FOLDER"]}/users/{userID}'
    response = make_response(send_from_directory(DP_FOLDER, user.dp))
    
    return response
