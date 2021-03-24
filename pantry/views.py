from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (
  Pantry, 
  Product,
  ShoppingList,
  ShoppingItem
)
from .serializers import (
  ProductSerializer, 
  PantrySerializer,
  ShoppingItemSerializer,
  ShoppingListSerializer
)

import jwt
import os

class ViewShoppingList(APIView):

  def post(self, request):

    try:
      #
      #
      #
      # Token
      try:
        token = request.data['token']
        decode = jwt.decode(token, os.getenv("SECRET"))
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
      # Pantry & Products
      try:
        pantry = Pantry.objects.get(kitchen=user)
        products = Product.objects.filter(pantry=pantry)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Pantry NO encontrada"
          }
        )
      #
      #
      #
      # Crea lista de compras
      lista = ShoppingListSerializer(data={
        "titulo": "Nueva lista",
	      "descripcion": "Descripcion",
        "pantry": pantry.id
      })

      if lista.is_valid():
        lista.save()

        for item in products:
          init = item.init
          current = item.current
          base = init/3

          if current <= base:

            # Crear item
            shoppingItem = {
              'lista' : lista.data['id'],
              'producto' : item.id,
              'titulo': item.nombre,
              'cantidad': item.init,
              'precio': item.precio
            }
            serialized = ShoppingItemSerializer(data=shoppingItem)
            if serialized.is_valid():
              serialized.save()
            else:
              return Response(
                status=status.HTTP_206_PARTIAL_CONTENT,
                data={
                  "multipass": False,
                  "detail": "Serialized Error",
                  "data": serialized.errors
                }
              )
        #
        #
        #
      else:
        return Response(
          status=status.HTTP_400_BAD_REQUEST,
          data=lista.errors
        )

      listaID = lista.data['id']
      shoppingItem = ShoppingItem.objects.filter(lista=listaID)

      # Valida si la lista contiene mas de un elemento
      if len(shoppingItem) > 0:
        serialized = ShoppingItemSerializer(shoppingItem, many=True)
        return Response(
          status=status.HTTP_200_OK,
          data=serialized.data
        )
      else:
        ShoppingList.objects.get(id=listaID).delete()
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": True,
            "detail": "No hay productos en la despensa pendientes por comprar"
          }
        )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data={
          "multipass": False
        }
      )

class ViewShoppingListGet(APIView):
  def post(self, request):

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
      # Lista de compras
      try:
        pantry = Pantry.objects.get(kitchen=user)
        shoppingList = ShoppingList.objects.filter(pantry=pantry)
      except:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={
            "multipass": False,
            "detail": "Despensa no encontrada"
          }
        )
      #
      #
      #
      # Serialized
      serialized = ShoppingListSerializer(shoppingList, many=True)
      return Response(
        status=status.HTTP_200_OK,
        data={
          "multipass": True,
          "detail": "Listas de compra",
          "data": serialized.data
        }
      )
    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data={
          "multipass": False
        }
      )








