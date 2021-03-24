from django.contrib.auth.models import User
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import jwt
import os

from .models import CustomUserModel
from .serializers import CustomUserSerializer, CustomUserSerializerSafety

from pantry.models import Pantry
from pantry.serializers import PantrySerializer

class CustomUser(APIView):

    def post(self,request):

        data = request.data
        serialized = CustomUserSerializer(data=data)

        if serialized.is_valid():
            
            # Crea usuario y hashea la contraseña
            serialized.save()
            user = CustomUserModel.objects.get(username=data['username'])
            user.set_password(data['password'])
            user.save()

            #
            #
            #
            # Crea una nueva Pantry
            pantry = PantrySerializer(data={"kitchen": user.id})
            if pantry.is_valid():
                pantry.save()
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "multipass": True,
                        "detail": "Usuario creado",
                        "data": {
                            "user": serialized.data,
                            "pantry": pantry.data
                        }
                    }
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "multipass": False,
                        "detail": "Error serialized",
                        "data": pantry.errors
                    }
                )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serialized.errors
        )

class GetUser(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:

            try:
                token = request.headers['authorization'].split(" ")[1]
                decode = jwt.decode(token, os.getenv('SECRET'))
            except:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={
                        "multipass": False,
                        "detail": "NO information"
                    }
                )

            user = CustomUserModel.objects.get(id=decode['user_id'])
            serialized = CustomUserSerializerSafety(user)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "multipass": True,
                    "detail": "Informacion del usuario",
                    "data": serialized.data
                }
            )
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )