from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Recipes, Ingredient, Method, Step
from .serializers import RecipesSerializer, IngredientSerializer

from pantry.models import Product, Pantry, ShoppingList, ShoppingItem
from pantry.serializers import ProductSerializer, ShoppingListSerializer, ShoppingItemSerializer

import jwt
import os


class ViewRecipes(APIView):

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

  def delete(self, request):
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
      # Receta
      try:
        receta = request.data['receta']
        receta = Recipes.objects.get(id=receta)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Receta no encontrada"
          }
        )
      #
      #
      #
      # Valida si la receta es propia
      print("===================> User", user,"===> Chef", receta.chef.id)
      if user != receta.chef.id:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "Receta no encontrada"
          }
        )
      else:
        receta.delete()
        return Response(
          status=status.HTTP_200_OK,
          data={
            "multipass": True,
            "detail": "Elemento eliminado",
            "data": {
              "receta": receta.titulo,
              "Chef": receta.chef.username
            }
          }
        )
        
    
    except:
      return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data={
          "multipass": False
        }
      )

  def patch(self, request):

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
      #
      # Receta
      try:
        receta = request.data['receta']
        receta = Recipes.objects.get(id=receta)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Receta no encontrada"
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
            "detail":"No data"
          }
        )
      #
      #
      #
      # Valida si la receta es propia
      if user != receta.chef.id:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "Receta no encontrada"
          }
        )
        #
        #
        #
        # PATCH
      else:
        serialized = RecipesSerializer(
          instance=receta,
          data=request.data['data'],
          partial=True
        )
        if serialized.is_valid():
          serialized.save()
          return Response(
            status=status.HTTP_200_OK,
            data={
              "multipass": True,
              "detail": "Elemento patcheado",
              "data": serialized.data
            }
          )
        else:
          return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
              "multipass": False,
              "detail": "Serialized error",
              "data": serialized.errors
            }
          )
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )

class ViewRecipesGet(APIView):

  def post(self, request):

    try:

      try:

        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv('SECRET'))
      
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED, 
          data={
            "multipass":False,
            "detail": "NO information"
          }
        )

      recipes = Recipes.objects.filter(chef=decode['user_id'])
      serialized = RecipesSerializer(recipes, many=True)

      if len(serialized.data) == 0:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail":"No tienes recetas"
          }
        )
      else:
        return Response(
          status=status.HTTP_200_OK,
          data={
            "multipass": True,
            "detail": "Tus recetas",
            "data": serialized.data
          }
        )
    except:

      
      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )



# Ejecuta una receta y resta los ingredientes usados en la despensa
class ViewRecipeTrigger(APIView):

  def post(self,request):

    try:

      try:
        token = request.headers['authorization'].split(" ")[1]
        decode = jwt.decode(token, os.getenv("SECRET"))
        user = decode['user_id']
      except:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "NO Information"
          }
        )

      try:
        id = request.data['receta']
        receta = Recipes.objects.get(id=id)
        ingredients = Ingredient.objects.filter(receta=receta)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No se encontro la receta",
          }
        )

      try:
        pantry = Pantry.objects.get(kitchen=user)
        products = Product.objects.filter(pantry=pantry)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No se encontro la despensa"
          }
        )

      # Valida si la receta pertenece al usuario
      if user != receta.chef.id:
        return Response(
          status=status.HTTP_401_UNAUTHORIZED,
          data={
            "multipass": False,
            "detail": "No se encontro la receta"
          }
        )

      #Creando lista para posibles productos pendientes
      listaInfo = {
        "titulo":"Lista de compras",
        "descripcion":"Debes primero comprar los ingredientes de esta lista.",
        "pantry": pantry.id
      }

      lista = ShoppingListSerializer(data=listaInfo)
      if lista.is_valid():
        lista.save()
      
        for ingredient in ingredients:

          ## INGREDIENTES

          # Si NO tiene referencia en la despensa
          # agrega el ingrediente a la lista creada.
          if ingredient.producto is None:
            itemInfo = {
              "lista":lista.data['id'],
              "titulo": ingredient.nombre,
              "cantidad": ingredient.cantidad
            }
          
            item = ShoppingItemSerializer(data=itemInfo)
            if item.is_valid():
              item.save()
          #
          #
          #
          # Si la cantidad del ingrediente, es mayor
          # al contenido del producto en la despensa
          # lo almacenta en la lista de compras.
          elif ingredient.cantidad > ingredient.producto.current:
            itemInfo = {
              "lista":lista.data['id'],
              "producto":ingredient.producto.id,
              "cantidad": ingredient.cantidad,
              "titulo": ingredient.nombre,
              "precio": ingredient.producto.precio,
            }

            item = ShoppingItemSerializer(data=itemInfo)
            if item.is_valid():
              item.save()
          #
          #
          #
          #
          # Si la cantidad del ingrediente es menor o
          # igual que el contenido del producto en la
          # despensa, se sustrae la cantidad utilizada.
          elif ingredient.cantidad <= ingredient.producto.current:
            current = ingredient.producto.current - ingredient.cantidad
            serialized = ProductSerializer(
              instance=ingredient.producto,
              data={"current": current},
              partial=True
            )

            if serialized.is_valid():
              serialized.save()
            


        # Lista de compras
        shoppingListItems = ShoppingItem.objects.filter(lista=lista.data['id'])

        # Si la lista tiene mas de un item retorna la lista
        # De lo contrario la elimina.
        if len(shoppingListItems) > 0:
          serialized = ShoppingItemSerializer(shoppingListItems, many=True)
          return Response(
            status=status.HTTP_409_CONFLICT,
            data= {
              "multipass": False,
              "detail": "Debes comprar estos ingredientes",
              "data": {
                "receta": receta.titulo,
                "ingredientes": serialized.data
              }
            }
          )
        else:
          newList = ShoppingList.objects.get(id=lista.data['id'])
          newList.delete()
          print("Lista eliminada")


      else:
        return Response(
          status=status.HTTP_406_NOT_ACCEPTABLE,
          data=lista.errors
        )

      if len(ingredients) == 0:
        return Response (
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "No hay ingredientes en la receta.",
            "data": {
              "receta": receta.titulo,
              "ingredientes": ingredients
            }
          }
        )
      serialized = ProductSerializer(products, many=True)
      return Response(
        status=status.HTTP_200_OK,
        data={
          "multipass": True,
          "detail": "La receta"
        }
      )
    
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )


