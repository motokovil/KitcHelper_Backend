from django.contrib.auth.models import User
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUserModel
from .serializers import CustomUserSerializer

class CustomUser(APIView):

    def post(self,request):
        data = request.data
        serialized = CustomUserSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            user = CustomUserModel.objects.get(username=data['username'])
            user.set_password(data['password'])
            user.save()
            return Response(
                data=serialized.data,
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serialized.errors
        )
    