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

eba = {"name": "Eba", "cuisine": "Nigeria",
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


from dotenv import load_dotenv
from os import getenv

load_dotenv()

USER = getenv("DB_USER")
HOST = getenv("DB_HOST")
PWD = getenv("DB_PWD")
DB = getenv("DB_NAME")
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models import storage
from models.user import User
from models.recipe import Recipe
from models.chat.chat import Chat
from models.chat.chatSession import ChatSession

engine = create_engine(
             f"mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}",
             pool_pre_ping=True)

sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
session = scoped_session(sessionFactory)

u = storage.getByEmail('ola@email.com')
s = storage.createChatSession(u.id, "Bread and Butter")

# >>> systemMessage = "Your name is Yishu. You are a food and nutrition specialist bot. You provide expert assistance on all matters related to food, nutrition and health"
# >>> chat = Chat(userID=user.id, chat={"role": "system", "content": systemMessage})
# >>> chat
# <models.chat.chat.Chat object at 0x7fc8cd2a5c60>
# >>> chat.toDict()
# {'userID': '2de148a6-3512-4654-a062-c0baa40f19db', 'chat': {'role': 'system', 'content': 'Your name is Yishu. You are a food and nutrition specialist bot. You provide expert assistance on all matters related to food, nutrition and health'}, 'id': 'e4354ae9-351b-4816-ac75-215374d7e2fd', 'createdAt': '2023-12-04T09:13:57.738085', 'updatedAt': '2023-12-04T09:13:57.738107'}
# >>> chat.save()
# WARNING: MYSQL_OPT_RECONNECT is deprecated and will be removed in a future version.
# >>> 


# curl -X POST 0:6000/api/v1/users -H 'Content-Type: application/json' -d '{"username": "Ola of da milky way", "password": "pass", "email": "ajebo@email.com", "junk": "filter this", "firstname": "Mike", "lastname": "Rock"}'
# curl 0:6000/api/v1/login -H 'Content-Type: application/json' -d '{"email": "mikerock@email.com", "password": "pass"}'


# curl "0:6000/api/v1/recipes?filter_by=cuisine+Nigerian,Ghanaian:serving+6:mike+wonderful&page=5&keyword=Jollof&detailed=true"

# curl -XPOST 0:6000/api/v1/recipes -H 'Content-Type: application/json' -H 'auth-token: 0768d7a0-1c77-4560-a501-b7da15345692' -d '{"name": "Eba", "cuisine": "Nigeria", "ingredients": ["2 Cups of Garri", "Boiled water"], "instructions": ["Dance around the room for 2 mins", "Do the Hokey Pokey"], "userID": "8bdfa62f-b226-4d6c-bd73-16c02c370a4d", "prep_time_minutes": 20, "cook_time_minutes": 40, "serving_size": 4, "calories_per_serving": 400}'
