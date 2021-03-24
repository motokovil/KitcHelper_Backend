from django.urls import path
from .views import ViewShoppingList, ViewShoppingListGet

urlpatterns = [
  path('ShoppingList/', ViewShoppingList.as_view()),
  path('ShoppingList/get/', ViewShoppingListGet.as_view())
]
