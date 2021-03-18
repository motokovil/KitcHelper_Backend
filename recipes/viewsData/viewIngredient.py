from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes, Ingredient, Method, Step
from recipes.serializers import IngredientSerializer

import jwt
import os



class ViewIngredientPost(APIView):

  def post(self, request):

    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv('SECRET'))

      id = request.data['receta']
      receta = Recipes.objects.get(id=id)

      ingredientes = request.data['ingredientes']

      if decode['user_id']==receta.chef.id:

        serialized = IngredientSerializer(
          data=ingredientes,
          many=True
        )

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
          
      else:

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )

class ViewIngredientGet(APIView):

  def post(self,request):
    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv('SECRET'))
      id = request.data['recipe']



      try:
        receta = Recipes.objects.get(id=id)
        ingredientes = Ingredient.objects.filter(receta=receta)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND
        )



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






      return Response(
          status=status.HTTP_200_OK
        )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST,
      )






