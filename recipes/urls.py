from django.urls import path
from .views import ViewRecipes, ViewRecipesGet

urlpatterns = [
    path('', ViewRecipes.as_view()),
    path('get/', ViewRecipesGet.as_view()),
]
