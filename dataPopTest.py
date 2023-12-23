#!/usr/bin/env python3

import json
# Load recipe data from file
with open('./dataset.json', 'r') as recipeData:
    data = json.load(recipeData)

# Create recipe objects and save to database
for recipe in data:
    if recipe.get("images"):
        for image in recipe["images"]:
            # dp = RecipeDP(recipeID=newRecipe.id, userID=user.id, fileType="link", filePath=image)
            # dp.save()
            print(image)
    else:
        # dp = RecipeDP(recipeID=newRecipe.id, userID=user.id)
        # dp.save()
        print("No image")
