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


# Valida si los ingredientes están en la despensa (Pantry)
# La cantidad de los ingredientes no sea mayor que lo disponible
# Retorna una lista de los ingredientes que no están disponibles
class ViewRecipeValidator(APIView):

  def post(self, request):
    
    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv("SECRET"))
      user = decode['user_id']

      receta = request.data['receta']
      ingredients = Ingredient.objects.filter(receta=receta)

      pantry = Pantry.objects.get(kitchen=user)


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
          #Valida si los ingredientes estan en la despensa
          if ingredient.producto is None:
            print("Its NONE")
            itemInfo = {
              "lista":lista.data['id'],
              "titulo": ingredient.nombre,
              "cantidad": ingredient.cantidad
            }
            # Almacenar y validar
            item = ShoppingItemSerializer(data=itemInfo)
            if item.is_valid():
              item.save()
              #
              #
              #
          elif ingredient.cantidad > ingredient.producto.current:
            # Almacena los productos insuficientes para la receta, en la lista de compras
            itemInfo = {
              "lista":lista.data['id'],
              "producto":ingredient.producto.id,
              "titulo": ingredient.nombre,
              "precio": ingredient.producto.precio,
            }

            item = ShoppingItemSerializer(data=itemInfo)
            if item.is_valid():
              item.save()





        # Lista de items vinculados a la lista
        shoppingListItems = ShoppingItem.objects.filter(lista=lista.data['id'])

        # Si la lista tiene mas de un item retorna la lista
        # De lo contrario la elimina.
        print(shoppingListItems)
        if len(shoppingListItems) >= 1:
          serialized = ShoppingItemSerializer(shoppingListItems, many=True)
          return Response(
            status=status.HTTP_409_CONFLICT,
            data=serialized.data
          )
        else:
          newList = ShoppingList.objects.get(id=lista.data['id'])
          newList.delete()
          print("Lista eliminada")

      else:

        return Response(
          status=status.HTTP_411_LENGTH_REQUIRED,
          data=lista.errors
        )


      return Response(
        status=status.HTTP_200_OK
      )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )


#Ejecuta una receta y resta los ingredientes usados en la despensa
class ViewRecipeTrigger(APIView):

  def post(self,request):

    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv("SECRET"))
      user = decode['user_id']

      receta = request.data['receta']
      ingredients = Ingredient.objects.filter(receta=receta)

      pantry = Pantry.objects.get(kitchen=user)
      products = Product.objects.filter(pantry=pantry)
      
      for ingredient in ingredients:

        if ingredient.cantidad <= ingredient.producto.current:
          current = ingredient.producto.current - ingredient.cantidad
          serialized = ProductSerializer(
            instance=ingredient.producto,
            data={"current": current},
            partial=True
          )

          if serialized.is_valid():
            serialized.save()

        else:
          pending = products.filter(current=0)
          Pro = ProductSerializer(pending, many=True)
          return Response(
            status=status.HTTP_409_CONFLICT,
            data=Pro.data
          )

      serialized = ProductSerializer(products, many=True)
      return Response(
        status=status.HTTP_200_OK,
        data=serialized.data
      )
    
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )


