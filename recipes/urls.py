from django.urls import path
from .views import (
    ViewRecipes, 
    ViewRecipesGet,
    ViewRecipeValidator,
    ViewRecipeTrigger
)

urlpatterns = [
    path('', ViewRecipes.as_view()),
    path('get/', ViewRecipesGet.as_view()),
    path('validate/', ViewRecipeValidator.as_view()),
    path('execute/', ViewRecipeTrigger.as_view()),
]
