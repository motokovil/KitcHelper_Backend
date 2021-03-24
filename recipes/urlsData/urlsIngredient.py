from django.urls import path
from ..viewsData.viewIngredient import ViewIngredientGet, ViewIngredients

urlpatterns = [
    path('', ViewIngredients.as_view()),
    path('get/', ViewIngredientGet.as_view()),
]
