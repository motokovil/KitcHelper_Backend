from django.urls import path
from ..viewsData.viewIngredient import ViewIngredientGet, ViewIngredientPost

urlpatterns = [
    path('', ViewIngredientPost.as_view()),
    path('get/', ViewIngredientGet.as_view()),
]
