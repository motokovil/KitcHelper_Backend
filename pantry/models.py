from django.db import models
from users.models import CustomUserModel





# PANTRY
class Pantry(models.Model):
  kitchen = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
  
  def __str__(self):
      return self.kitchen.username
  



# PRODUCT
class Product(models.Model):

  LITER = 'lt'
  GRAM = 'gr'
  MILLILITER = 'ml'
  UNIT = 'un'
  KILOGRAM = 'kg'

  MEASURES_AVAILABLE = [
    (LITER, 'Litro'),
    (GRAM, 'Gramo'),
    (MILLILITER, 'Mililitro'),
    (UNIT, 'Unidad'),
    (KILOGRAM, 'Kilogramo')
  ]

  nombre = models.CharField(max_length=200)
  pantry = models.ForeignKey(Pantry,on_delete=models.CASCADE)
  precio = models.IntegerField()
  init = models.IntegerField()
  current = models.IntegerField()
  medida = models.CharField(
    max_length=2,
    choices = MEASURES_AVAILABLE,
    default=GRAM
  )

  def __str__(self):
      return self.nombre




# SHOPPING LIST
class ShoppingList(models.Model):
  titulo = models.CharField(max_length=200)
  descripcion = models.TextField(max_length=400)
  activa = models.BooleanField(default=True)
  pantry = models.ForeignKey(
    Pantry, 
    on_delete=models.CASCADE,
    blank=True,
    null=True
  )

  def __str__(self):
      return self.titulo


  

#SHOPPING ITEM
class ShoppingItem(models.Model):
  lista = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
  titulo = models.CharField(max_length=200)
  cantidad = models.IntegerField()
  precio = models.IntegerField(
    null=True,
    blank=True
  )
  producto = models.ForeignKey(
    Product, 
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  def __str__(self):
      return self.titulo
  











