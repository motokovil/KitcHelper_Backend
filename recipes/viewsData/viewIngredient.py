from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes, Ingredient, Method, Step
from recipes.serializers import IngredientSerializer

import jwt
import os



class ViewIngredients(APIView):

  def post(self, request):

    try:

      # Token
      try:
        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv('SECRET'))
        user = decode['user_id']
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "NO information"
          }
        )

      # Receta
      try:
        id = request.data['receta']
        receta = Recipes.objects.get(id=id)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No se encontró la receta"
          }
        )
      
      # Ingrediente
      try:
        ingredientes = request.data['ingredientes']
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Faltan los ingredientes"
          }
        )

      # Valida si la receta es propia
      if user == receta.chef.id:

        for ingredient in ingredientes:
          ingredient['receta'] = receta.id
        #
        #
        #
        serialized = IngredientSerializer(
          data=ingredientes,
          many=True
        )
        # Valida
        if serialized.is_valid():
          serialized.save()
          return Response(
            status=status.HTTP_201_CREATED,
            data={
              "multipass": True,
              "detail": "Se agregaron los ingredientes",
              "data": serialized.data
            }
          )
        else:
          return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serialized.errors
          )
        #
        # 
        #  
      else:

        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "No se encontró la receta"
          }
        )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )

  def patch(self,request):

    try:
      #
      #
      #
      # Token
      try:
        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv('SECRET'))
        user = decode['user_id']
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "NO information"
          }
        )
      #
      #
      #
      # Ingrediente
      try:
        ingrediente = request.data['ingrediente']
        ingrediente = Ingredient.objects.get(id=ingrediente)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Ingrediente NO encontrado"
          }
        )
      #
      #
      #
      # Data
      try:
        data = request.data['data']
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No data"
          }
        )
      #
      #
      #
      # Valida si el ingrediente es de una receta propia
      if user != ingrediente.receta.chef.id:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "Ingrediente NO encontrado"
          }
        )
      else:
        serialized = IngredientSerializer(
          instance = ingrediente,
          data = data,
          partial = True
        )
        if serialized.is_valid():
          serialized.save()
          return Response(
            status=status.HTTP_200_OK,
            data={
              "multipass": True,
              "detail": "Elemento actualizado",
              "data": serialized.data
            }
          )
        else: 
          return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
              "multipass": False,
              "detail": "Elemento No actualizado",
              "data": serialized.errors
            }
          )


    except:
      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )

  def delete(self,request):

    try:
      # 
      #
      #
      # Token
      try:
        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv('SECRET'))
        user = decode['user_id']
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "NO information"
          }
        )
      # 
      #
      #
      # Ingrediente
      try:
        ingrediente = request.data['ingrediente']
        ingrediente = Ingredient.objects.get(id=ingrediente)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Ingrediente NO encontrado"
          }
        )
      #
      #
      #
      # Valida si el ingrediente es de una receta propia
      if user != ingrediente.receta.chef.id:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "Ingrediente NO encontrado"
          }
        )
      else:
        ingrediente.delete()
        return Response(
          status=status.HTTP_200_OK,
          data={
            "multipass": True,
            "detail": "Elemento fue eliminado",
            "data": {
              "Ingrediente": ingrediente.nombre,
              "receta": ingrediente.receta.titulo
            }
          }
        )
    
    except:
      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )




class ViewIngredientGet(APIView):

  def post(self,request):
    try:
      #
      #
      #
      # Token

      try:
        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv('SECRET'))
        user = decode['user_id']
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "NO information"
          }
        )
      #
      #
      #
      # Recipe
      try:
        id = request.data['recipe'],
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Proporciona la receta"
          }
        )


      # Obtiene los ingredientes de la receta o NOT FOUND
      try:
        print("LA RECETA ID:", id[0])
        receta = Recipes.objects.get(id=id[0])
        print(receta.titulo)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No se encontro esa receta",
          }
        )
      
      try:
        
        ingredientes = Ingredient.objects.filter(receta=receta)
      except:
        print("EXCEPT INGREDIENTES <======###")
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No se encontraron los ingredientes"
          }
        )



      if user == receta.chef.id:
        print("USER == CHEF <======###")
        serialized = IngredientSerializer(ingredientes, many=True)
        
        if len(ingredientes) == 0:
          return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
              "multipass": False,
              "detail": "No tiene ingredientes aún",
              "data": {
                "receta": receta.titulo
              }
            }
          )
        else:
          return Response(
            status=status.HTTP_200_OK,
            data={
              "multipass": True,
              "detail": "Los ingredientes de la receta",
              "data": {
                "receta": receta.titulo,
                "ingredientes":serialized.data
              }
            }
          )
      else:

        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "datail": "No se encontro esa receta"
          }
        )






      return Response(
          status=status.HTTP_200_OK
        )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST,
      )






