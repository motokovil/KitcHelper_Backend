from rest_framework.serializers import ModelSerializer
from .models import Recipes

class RecipesSerializer(ModelSerializer):
  class Meta:
    model = Recipes
    fields = ('__all__')