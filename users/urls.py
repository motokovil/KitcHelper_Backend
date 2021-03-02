from django.urls import path
from .views import CustomUser

urlpatterns = [
    path('', CustomUser.as_view())
]
