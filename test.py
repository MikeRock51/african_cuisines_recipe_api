from models import storage
from models.user import User
from models.recipe import Recipe
from models.roles import UserRole
from sqlalchemy.exc import IntegrityError

mike = {'firstname': 'Michael', 'lastname': 'Adebayo', 'username': 'Mike Rock', 'email': 'mikerock@email.com',
        'phone': '0885465549', 'address': 'Abuja', 'password': 'pass', "role": UserRole.admin}
user = User(**mike)
user.save()

eba = {"recipe_name": "Eba", "cuisine": "Nigeria",
       "ingredients": ["2 Cups of Garri", "Boiled water"],
       "instructions": ["Dance around the room for 2 mins", "Do the Hokey Pokey"], "userID": user.id,
       "prep_time_minutes": 20,
       "cook_time_minutes": 40,
       "serving_size": 4,
       "calories_per_serving": 400}
food = Recipe(**eba)
food.save()

user2 = User(**mike)

try:
    user2.save()
except IntegrityError as e:
    error_message = str(e.args[0])
    start_index = error_message.find('"')
    end_index = error_message.rfind('"')
    if start_index != -1 and end_index != -1:
        extracted_message = error_message[start_index + 1:end_index]
        print(extracted_message)
    else:
        print(error_message)
