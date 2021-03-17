from django.contrib import admin
from .models import (
  Recipes,
  Ingredient,
  Method,
  Step
)

admin.site.register(Recipes)
admin.site.register(Ingredient)
admin.site.register(Method)
admin.site.register(Step)