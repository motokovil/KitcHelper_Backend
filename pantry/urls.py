from django.urls import path
from .views import ViewShoppingList

urlpatterns = [
  path('ShoppingList/', ViewShoppingList.as_view())
]
