from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class NutritionalValue(BaseModel, Base):
    __tablename__ = "nutritional_values"

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    recipeID = Column(String(60), ForeignKey('recipes.id'), nullable=False)
    dps = relationship('NutritionDP', backref='nutrition', cascade='all, delete-orphan', single_parent=True)
    UniqueConstraint('name', 'recipeID', name='unique_recipe_nutrition')

    def toDict(self, detailed=False):
        """Extension of basemodel.toDict for nutrition data"""
        instance = super().toDict()
        instance['nutritions_dps'] = [dp.toDict() for dp in self.dps]
        if detailed:
            return instance

        heldBackAttrs = ["__class__", "createdAt", "updatedAt"]

        # Filter heldback attributes
        for attr in heldBackAttrs:
            if attr in instance:
                instance.pop(attr)

        return instance
