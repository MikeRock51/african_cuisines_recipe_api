#!/usr/bin/env python3
"""The database engine"""

from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, and_
from typing import Dict
from dotenv import load_dotenv
from math import ceil
from sqlalchemy.exc import ArgumentError

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
        if obj:
            # Set the starting point of data to retrieve
            offset = (page - 1) * size
            tableName = obj.__tablename__

            try:
                query = self.__session.query(obj)
                if tableName == 'recipes':
                    # Filter data by search keyword
                    query = query.filter(obj.name.like(f"%{search}%"))
                if filterColumns != {}:
                    # Create a list of filter conditions based on specified columns
                    filterConditions = [(key.in_(value)
                                         for key, value in filterColumns.items())]
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

    def get(self, obj, id: str):
        """Retrieves the obj instance with the given id"""
        models = self.allModels()

        if obj in models.values():
            instance = self.__session.query(obj).filter(obj.id == id).first()
            return instance

    def getByEmail(self, email: str):
        """Retrieves the user with the given email from database"""
        User = self.allModels()['User']
        user = self.__session.query(User).filter_by(email=email).one()
        return user

    def close(self) -> None:
        """Removes the current session"""
        self.__session.remove()
