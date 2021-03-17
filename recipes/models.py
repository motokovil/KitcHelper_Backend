from django.db import models
from users.models import CustomUserModel
from pantry.models import Product




#RECIPES
class Recipes(models.Model):
  titulo = models.CharField(max_length=200)
  chef = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo




#INGREDIENT
class Ingredient(models.Model):
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
  cantidad = models.IntegerField()
  receta = models.ForeignKey(Recipes, on_delete=models.CASCADE)
  producto = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
  medida = models.CharField(
    max_length=2,
    choices = MEASURES_AVAILABLE,
    default=GRAM
  )
  
  def __str__(self):
      return self.nombre




#METHOD
class Method(models.Model):
  titulo = models.CharField(max_length=200)
  receta = models.ForeignKey(Recipes, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo




#STEP
class Step(models.Model):
  titulo = models.CharField(max_length=200)
  posicion = models.IntegerField(default=0)
  descripcion = models.TextField(max_length=530)
  tiempo = models.IntegerField()
  preparacion = models.ForeignKey(Method, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo
  