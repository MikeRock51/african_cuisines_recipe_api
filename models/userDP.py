#!/usr/bin/env python3
"""The user display picture model"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class UserDP(BaseModel, Base):
    """Defines a user DP object"""

    __tablename__ = 'user_dps'

    filePath = Column(String(384), nullable=False, default="https://icons.iconarchive.com/icons/graphicloads/colorful-long-shadow/256/User-icon.png")
    fileType = Column(String(30), nullable=False, default="link")
    userID = Column(String(60), ForeignKey('users.id'), nullable=False)
    # user = relationship('User', backref='dp', cascade='all, delete', uselist=False)
