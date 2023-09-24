from models import storage
from models.user import User
from models.recipe import Recipe
mike = {'firstname': 'Michael', 'lastname': 'Adebayo', 'email': 'mikerock@email.com',
        'phone': '0885465549', 'address': 'Abuja', 'password': 'pass'}
eba = {"recipe_name": "Eba", "cuisine": "Nigeria",
       "ingredients": ["2 Cups of Garri", "Boiled water"],
       "instructions": ["Dance around the room for 2 mins", "Do the Hokey Pokey"],
       "prep_time_minutes": 20,
       "cook_time_minutes": 40,
       "serving_size": 4,
       "calories_per_serving": 400}
food = Recipe(**eba)
