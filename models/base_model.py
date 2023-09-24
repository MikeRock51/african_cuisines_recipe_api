#!/usr/bin/env python3

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class BaseModel:
    """Defines common methods and attributes inheritted by other models"""
    id = Column(String(60), primary_key=True, nullable=False)
    createdAt = updatedAt = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Object constructor"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['updatedAt', 'createdAt']:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

        self.id = str(uuid4())
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def __str__(self) -> str:
        """Returns a string representation of an instance"""
        return f"[{self.__class__.__name__}: ({self.id})] -> {self.__dict__}"



model = BaseModel()
print(model)
# print(model.id, model.createdAt, model.updatedAt)
