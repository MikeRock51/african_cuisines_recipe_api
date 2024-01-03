from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class NutritionalValue(BaseModel, Base):
    __tablename__ = "nutritional_values"

    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    dps = relationship('NutritionDP', backref='nutrition', cascade='all, delete-orphan', single_parent=True)
    UniqueConstraint('title', 'recipeID', name='unique_recipe_nutrition')
