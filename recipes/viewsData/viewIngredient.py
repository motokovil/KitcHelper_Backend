from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes, Measure, Ingredient, Method, Step
from recipes.serializers import IngredientSerializer

import jwt
import os

class ViewIngredient(APIView):

  def post(self,request):
    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv('SECRET'))

      id = request.data['recipe']
      receta = Recipes.objects.get(id=id)
      ingredientes = Ingredient.objects.filter(receta=receta)

      if decode['user_id'] == receta.chef.id:
        serialized = IngredientSerializer(ingredientes, many=True)

        return Response(
          status=status.HTTP_200_OK,
          data=serialized.data
        )
      else:

        return Response(
          status=status.HTTP_401_UNAUTHORIZED
        )
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST,
      )