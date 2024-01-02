#!/usr/bin/env python3
"""Index views"""

from api.v2.views import app_views
from flask import jsonify, request
from flasgger import swag_from


@app_views.route('/status')
def getStatus():
    """
    Returns the status of the server
    responses:
      200:
        description: All systems green!
    """
    return jsonify({
        "status": "success",
        "message": "All systems green!"
    })

@app_views.route('/test', methods=['POST'])
def testBody():
    """
    Returns the status of the server
    responses:
      200:
        description: All systems green!
    """
    data = request.form.to_dict()
    print(data)
    
    return jsonify({
        "status": "success",
        "message": "All systems green!",
        # "data": name
    })

@app_views.route('/upload', methods=['POST'])
def upload():
    recipe_images = request.files.getlist('recipe_images[]')
    ingredient_images = request.files.getlist('ingredient_images[]')
    instruction_images = request.files.getlist('instruction_images[]')

    print(recipe_images)

    # Process each category of files as needed
    for file in recipe_images:
        print(file)
        # if file.filename != '':
        #     file.save(f"uploads/recipe_images/{file.filename}")

    for file in ingredient_images:
        print(file)
        # if file.filename != '':
            # file.save(f"uploads/ingredient_images/{file.filename}")

    for file in instruction_images:
        print(file)
        # if file.filename != '':
        #     file.save(f"uploads/instruction_images/{file.filename}")

    return 'Files uploaded successfully'
