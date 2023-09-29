#!/usr/bin/env python3

from models import storage
from models.user import User
from models.recipe import Recipe
from models.roles import UserRole
from sqlalchemy.exc import IntegrityError
import json

mike = {'firstname': 'Michael', 'lastname': 'Adebayo',
        'username': 'Mike Rock', 'email': 'mikerock@email.com',
        'phone': '08107094647', 'address': 'Abuja',
        'password': 'pass', "role": UserRole.admin}

# Create user if it doesn't exist
try:
    user = User(**mike)
    user.save()
except IntegrityError:
    # If user exist, retrieve the user
    storage.reload()
    user = storage.getByEmail(mike['email'])

# Load recipe data from file
with open('./dataset.json', 'r') as recipeData:
    data = json.load(recipeData)

error = False
# Create recipe objects and save to database
for recipe in data:
    try:
        newRecipe = Recipe(**recipe)
        newRecipe.userID = user.id
        newRecipe.save()
    except Exception as e:
        print(e)
        print(recipe)
        error = True
        break

if not error:
    print('Mission Accomplished!!!')
else:
    print('An error occurred')
