from rest_framework.serializers import ModelSerializer
from .models import Recipes, Ingredient, Measure

class RecipesSerializer(ModelSerializer):
  class Meta:
    model = Recipes
    fields = ('__all__')


class IngredientSerializer(ModelSerializer):
  class Meta:
    model = Ingredient
    fields = ('__all__')

class MeasureSerializer(ModelSerializer):
  class Meta:
    model = Measure
    fields = ('__all__')