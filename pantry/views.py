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

    print("╔══╦╗░░░░░░╔╗░░░░░╔╗╔╦═╦╗░")
    print("║══╣╚╦═╦═╦═╬╬═╦╦═╗║║╠╣═╣╚╗")
    print("╠══║║║╬║╬║╬║║║║║╬║║╚╣╠═║╔╣")
    print("╚══╩╩╩═╩═╣╔╩╩╩═╬╗║╚═╩╩═╩═╝")
    print("░░░░░░░░░╚╝░░░░╚═╝░░░░░░░░")

    try:

      token = request.data['token']
      decode = jwt.decode(token, os.getenv("SECRET"))
      user = decode['user_id']

      pantry = Pantry.objects.get(kitchen=user)
      products = Product.objects.filter(pantry=pantry)


      shoppingList = list()
      print("")
      print(" ╔╗ ")
      print("╔╝║ ")
      print("╚╗║ ")
      print(" ║║ ")
      print("╔╝╚╗")
      
      
      print("===========>> CREANDO NUEVA LISTA <<============")
      data = request.data
      data['pantry'] = pantry.id
      lista = ShoppingListSerializer(data=data)

      if lista.is_valid():
        lista.save()
        print(lista.data)
        print("==========>> Lista Terminada <<===========")


        
        print("╔═══╗")
        print("║╔═╗║")
        print("╚╝╔╝║")
        print("╔╝ ╔╝")
        print("║ ╚═╗")

        for item in products:
          init = item.init
          current = item.current
          base = init/3

          if current <= base:
            print("")
            print(f"=====>> Creando Item {item} <<======")

            # Crear item
            shoppingItem = {
              'lista' : lista.data['id'],
              'producto' : item.id
            }
            serialized = ShoppingItemSerializer(data=shoppingItem)
            if serialized.is_valid():
              serialized.save()
              print(f"=====>> Item {item} <<======")
            
            else:
              print(f"=====>> Item {item} NO guardado <<======")     
      
      else:

        print("=========== Lista NO fue creada ============")
        print("")
        print("")
        return Response(
          status=status.HTTP_400_BAD_REQUEST,
          data=lista.errors
        )

      shoppingItem = ShoppingItem.objects.filter(lista=lista.data['id'])
      serialized = ShoppingItemSerializer(shoppingItem, many=True)
      return Response(
        status=status.HTTP_200_OK,
        data=serialized.data
      )

    except:

      return Response(
        status=status.HTTP_400_BAD_REQUEST
      )