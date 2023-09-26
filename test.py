from models import storage
from models.user import User
from models.recipe import Recipe
from models.roles import UserRole
from sqlalchemy.exc import IntegrityError
from api.v1.utils import extractErrorMessage

ola = {'firstname': 'Michael', 'lastname': 'Olasunkanmi', 'username': 'Ollywayne', 'email': 'ola@email.com',
        'phone': '0885465549', 'address': 'Abuja', 'password': 'pass'}

user = User(**ola)
user.save()

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
    print(extractErrorMessage(e.args[0]))


from os import getenv
>>> USER = getenv("DB_USER")
>>> HOST = getenv("DB_HOST")
>>> PWD = getenv("DB_PWD")
>>> DB = getenv("DB_NAME")
>>> from sqlalchemy.orm import scoped_session, sessionmaker
>>> from sqlalchemy import create_engine
>>> engine = create_engine(
...             f"mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}",
...             pool_pre_ping=True)

sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
>>> session = scoped_session(sessionFactory)

curl -X POST 0:6000/api/v1/users -H 'Content-Type: application/json' -d '{"username": "Ola of da milky way", "password": "pass", "email": "ajebo@email.com", "junk": "filter this", "firstname": "Mike", "lastname": "Rock"}'
