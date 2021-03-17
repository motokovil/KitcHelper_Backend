from django.contrib import admin
from pantry.models import (
  Pantry, 
  Product,
  ShoppingItem,
  ShoppingList,
)

# Register your models here.
admin.site.register(Pantry)
admin.site.register(Product)
admin.site.register(ShoppingItem)
admin.site.register(ShoppingList)