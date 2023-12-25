from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint

class Upvote(BaseModel, Base):
    __tablename__ = "upvotes"

    userID = Column(String(60), ForeignKey('users.id'), nullable=False)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    UniqueConstraint('userID', 'recipeID', name='unique_user_recipe')
