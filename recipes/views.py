from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Recipes, Measure, Ingredient, Method, Step
from .serializers import RecipesSerializer

import jwt
import os


class ViewRecipes(APIView):

  def post(self, request):

    try:
      token = request.data['token']
      decode = jwt.decode(token, os.getenv('SECRET'))

      data = request.data
      data['chef'] = decode['user_id']

      serialized = RecipesSerializer(data=data)
      if serialized.is_valid():
        serialized.save()
        return Response(
          status=status.HTTP_201_CREATED,
          data=serialized.data
        )
      else:
        return Response(
          status=status.HTTP_400_BAD_REQUEST,
          data=serialized.errors
        )

    except:
      return Response(
        status=status.HTTP_400_BAD_REQUEST,
      )


class ViewRecipesGet(APIView):

  def post(self, request):

    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv('SECRET'))

      recipes = Recipes.objects.filter(chef=decode['user_id'])
      serialized = RecipesSerializer(recipes, many=True)

      return Response(
        status=status.HTTP_200_OK,
        data=serialized.data
      )
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )
