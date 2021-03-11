from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes, Measure, Ingredient, Method, Step
from recipes.serializers import MeasureSerializer

import jwt
import os


class ViewMeasureGet(APIView):

  def get(self, request):

  

    medidas = Measure.objects.all()
    print(medidas)

    serialized = MeasureSerializer(medidas, many=True)
    

    return Response(
      status=status.HTTP_200_OK,
      data=serialized.data
    )

    