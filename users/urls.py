from django.urls import path
from .views import CustomUser, GetUser


urlpatterns = [
    path('', CustomUser.as_view()),
    path('get/', GetUser.as_view()),
]
