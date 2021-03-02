from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel

class CustomUserSerializer(ModelSerializer):
  class Meta:
    model = CustomUserModel
    fields = ('username', 'password','email')