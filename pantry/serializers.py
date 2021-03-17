from rest_framework.serializers import ModelSerializer
from .models import (
  Product, 
  Pantry, 
  ShoppingItem, 
  ShoppingList
)


class ProductSerializer(ModelSerializer):
  class Meta:
    model = Product
    fields = ("__all__")

class PantrySerializer(ModelSerializer):
  class Meta:
    model = Pantry
    fields = ("__all__")

class ShoppingListSerializer(ModelSerializer):
  class Meta:
    model = ShoppingList
    fields = ("__all__")

class ShoppingItemSerializer(ModelSerializer):
  class Meta:
    model = ShoppingItem
    fields = ("__all__")




