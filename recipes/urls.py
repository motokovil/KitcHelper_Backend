from django.urls import path
from .views import ViewRecipes

urlpatterns = [
    path('', ViewRecipes.as_view())
]
