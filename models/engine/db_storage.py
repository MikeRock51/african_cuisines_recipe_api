#!/usr/bin/env python3
"""The database engine"""

from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, and_, func
from typing import Dict
from dotenv import load_dotenv
from math import ceil
from sqlalchemy.exc import ArgumentError, NoResultFound, IntegrityError
from sqlalchemy.sql.sqltypes import JSON
from os import path

load_dotenv()

USER = getenv("DB_USER")
HOST = getenv("DB_HOST")
PWD = getenv("DB_PWD")
DB = getenv("DB_NAME")


class DBStorage:
    """Defines the db storage object"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        # Create database engine
        self.__engine = create_engine(
            f"mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}",
            pool_pre_ping=True)

    def reload(self) -> None:
        """
            Creates all database table if not
            exists and establishes a new session
        """
        from models.base_model import Base
        allModels = self.allModels()

        Base.metadata.create_all(self.__engine)
        sessionFactory = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        self.__session = scoped_session(sessionFactory)
        Base.query = self.__session.query_property()

    def all(self, obj=None) -> Dict:
        """
            Retrieves all instances of obj or all entries from
            database if obj is None
        """
        objects = {}

        if obj:
            query = self.__session.query(obj).all()

            for result in query:
                key = f"{result.__class__.__name__}.{result.id}"
                objects[key] = result
        else:
            models = self.allModels()
            for model in models.values():
                query = self.__session.query(model).all()
                for result in query:
                    key = f"{result.__class__.__name__}.{result.id}"
                    objects[key] = result

        return objects

    def getPaginatedData(self, obj=None, page: int = 1,
                         size: int = 10, search="", filterColumns={}) -> Dict:
        """Retrieves paginated data"""
        Recipe = self.allModels()['Recipe']
        if obj:
            # Set the starting point of data to retrieve
            offset = (page - 1) * size
            tableName = obj.__tablename__

            try:
                query = self.__session.query(obj)
                if tableName == 'recipes':
                    # Filter data by search keyword
                    query = query.filter(obj.name.ilike(f"%{search}%"))
                if filterColumns != {}:
                    # Create a list of filter conditions based on specified columns
                    print(filterColumns)
                    
                    # filterConditions = [(key.in_(value)
                    #                      for key, value in filterColumns.items())]
                    filterConditions = []

                    for key, value in filterColumns.items():
                        if isinstance(key.type, JSON):
                            for val in value:
                                searchTerm = f'%{val}%'
                                filterConditions.append(key.ilike(searchTerm))
                        else:
                            filterConditions.append(key.in_(value))

                    # Filter data by specified columns
                    query = query.filter(and_(*filterConditions))

                    """filterConditions = [(key.in_(value) if
                                         hasattr(value, '__iter__') else (
                        key == value) for key, value in filterColumns.items())]"""

                total_pages = ceil(len(query.all()) / size)
                # Paginate query
                result = query.offset(offset).limit(size).all()

                return {
                    "data": result,
                    "page": page,
                    "page_size": size,
                    "total_items": len(result),
                    "total_pages": total_pages
                }
            except ArgumentError:
                raise ValueError('Invalid filters!')

    def allModels(self) -> Dict:
        """Returns a dictionary of all models"""
        from models.user import User
        from models.recipe import Recipe
        from models.chat.chat import Chat
        from models.chat.chatSession import ChatSession
        # from models.userDP import UserDP
        from models.recipeDP import RecipeDP
        from models.ingredients.ingredient import Ingredient
        from models.ingredients.ingredientDP import IngredientDP
        from models.instructions.instructionMedia import InstructionMedia
        from models.instructions.instruction import Instruction
        from models.instructions.videoInstruction import VideoInstruction
        from models.nutritions.nutritionalValue import NutritionalValue
        from models.nutritions.nutritionDP import NutritionDP
        from models.upvote import Upvote
        from models.bookmarks.bookmark import Bookmark
        from models.bookmarks.bookmarkList import BookmarkList
        from models.review import Review

        return {
            "User": User,
            "Recipe": Recipe,
            "Chat": Chat,
            "ChatSession": ChatSession,
            "RecipeDP": RecipeDP,
            "Ingredient": Ingredient,
            "IngredientDP": IngredientDP,
            "Instruction": Instruction,
            "InstructionMedia": InstructionMedia,
            "NutritionalValue": NutritionalValue,
            "NutritionDP": NutritionDP,
            "Upvote": Upvote,
            "Review": Review,
            "VideoInstruction": VideoInstruction,
            "Bookmark": Bookmark,
            "BookmarkList": BookmarkList
        }

    def new(self, obj) -> None:
        """Adds the given object to the current session"""
        self.__session.add(obj)

    def save(self) -> None:
        """Commits the state of the current session to database"""
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """Deletes obj from the current session and database"""
        from api.v2.utils import Utils
        if obj:
            self.__session.delete(obj)
            self.save()

            if obj.__class__.__name__ == 'Recipe':
                filedFields = ['ingredients', 'instructions', 'nutritional_values']
                DP_FOLDER = path.abspath('api/v2/assets/dps')
                for dp in obj.dps:
                    if dp.fileType != 'link':
                        Utils.deleteFile(f'{DP_FOLDER}/recipes/{obj.id}/{dp.filePath}')
                for field in filedFields:
                    items = getattr(obj, field)
                    for item in items:
                        if field == 'instructions':
                            fileObjects = item.medias
                        else:
                            fileObjects = item.dps
                        for file in fileObjects:
                            if file.fileType != 'link':
                                Utils.deleteFile(f'{DP_FOLDER}/{field}/{item.id}/{file.filePath}')
                VIDEO_FOLDER = path.abspath('api/v2/assets/videos')
                for vid in obj.videoInstructions:
                    if vid.fileType != 'link':
                        Utils.deleteFile(f'{VIDEO_FOLDER}/video_instructions/{vid.id}/{vid.filePath}')

    def get(self, obj, id: str):
        """Retrieves the obj instance with the given id"""
        models = self.allModels()

        if obj in models.values():
            instance = self.__session.query(obj).filter(obj.id == id).first()
            return instance

    def getByItemID(self, obj, item, id: str):
        """Retrieves all obj instances with the given item id"""
        models = self.allModels()

        if obj in models.values():
            instance = self.__session.query(obj).filter(
                getattr(obj, item) == id).all()
            return instance

    def getByEmail(self, email: str):
        """Retrieves the user with the given email from database"""
        try:
            User = self.allModels()['User']
            user = self.__session.query(User).filter_by(email=email).one()
            return user
        except NoResultFound:
            raise ValueError("User does not exist")

    def createChatSession(self, userID, topic=None):
        """Creates a chat sessiion for new users and prepopulates the chat history with system message"""
        from api.v1.utils import VError

        ChatSession = self.allModels()['ChatSession']
        Chat = self.allModels()['Chat']
        systemMessage = "Your name is Yishu. You are a food and nutrition specialist bot for Vital Vittles (Vital vittles is a food and nutrition web application, we provide assistance to users on african cuisines primarily, as well as other cuisines in the world.). You provide expert assistance on all matters related to food, nutrition and health"
        try:
            session = ChatSession(userID=userID, topic=topic)
            chat = Chat(userID=userID, sessionID=session.id,
                        content=systemMessage, role="system")
            session.save()
            chat.save()
            return [session.toDict()]
        except IntegrityError:
            raise VError("This chat topic already exist", 409)

    def getChatHistory(self, sessionID, userID):
        """Retrieves the chat history based on sessionID"""
        from api.v1.utils import VError
        ChatSession = self.allModels()['ChatSession']
        session = self.__session.query(
            ChatSession).filter_by(id=sessionID).first()

        if not session:
            raise VError("Chat session not found", 404)
        elif session.userID != userID:
            raise VError(
                "You are not authorized to access this chat session", 401)

        history = [chat.toDict() for chat in session.chats]
        return sorted(history, key=lambda x: x.get('createdAt', ''))

    def getUserSessions(self, userID):
        """Retrieves all chat sessions based on userID"""
        try:
            ChatSession = self.allModels()['ChatSession']
            chatHistory = self.__session.query(ChatSession).filter_by(
                userID=userID).order_by(ChatSession.updatedAt.desc()).all()
            return [chat.toDict() for chat in chatHistory]
        except Exception as e:
            raise ValueError(e)

    def close(self) -> None:
        """Removes the current session"""
        self.__session.remove()
