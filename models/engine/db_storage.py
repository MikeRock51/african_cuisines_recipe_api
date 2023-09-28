#!/usr/bin/env python3
"""The database engine"""

from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from typing import Dict
from dotenv import load_dotenv

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
    
    def getPaginatedData(self, obj=None, page: int = 1, size: int = 20, keyword="", filter_columns={}) -> Dict:
        """Retrieves paginated data"""
        if obj:
            data = []
            offset = (page - 1) * size

            query = self.__session.query(obj).filter(obj.name.like(f"%{keyword}%"))
            if filter_columns != {}:
                filter_conditions = None

            offset(offset).limit(size).all()

            for result in query:
                data.append(result.toDict())

            return {
                    "data": data,
                    "page": page,
                    "page_size": size,
                    "total_items": len(data),
                    "total_pages": self.__session.query(obj).count()
            }
 
    def allModels(self) -> Dict:
        """Returns a dictionary of all models"""
        from models.user import User
        from models.recipe import Recipe

        return {
                "User": User,
                "Recipe": Recipe
        }

    def new(self, obj) -> None:
        """Adds the given object to the current session"""
        self.__session.add(obj)

    def save(self) -> None:
        """Commits the state of the current session to database"""
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """Deletes obj from the current session and database"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def get(self, cls, id: str):
        """
            Retrieves the cls instance with the given id
            or None if no instance was found
        """
        models = self.allModels()

        if cls not in models.values():
            return None

        instances = self.all(cls)

        for instance in instances.values():
            if instance.id == id:
                return instance

    def getByEmail(self, email: str):
        """Retrieves the user with the given email from database"""
        User = self.allModels()['User']
        user = self.__session.query(User).filter_by(email=email).one()
        return user

    def close(self) -> None:
        """Removes the current session"""
        self.__session.remove()
