from django.urls import path
from .views import (
  ViewShoppingList, 
  ViewShoppingListGet,
  ViewProduct
)

urlpatterns = [
  path('Product/', ViewProduct.as_view()),
  path('ShoppingList/', ViewShoppingList.as_view()),
  path('ShoppingList/get/', ViewShoppingListGet.as_view())
]
