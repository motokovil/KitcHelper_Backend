from django.urls import path
from ..viewsData.viewIngredient import ViewIngredient

urlpatterns = [
    path('', ViewIngredient.as_view())
]
