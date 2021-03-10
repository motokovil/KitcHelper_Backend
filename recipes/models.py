from django.db import models
from users.models import CustomUserModel

# Create your models here.
class Recipes(models.Model):
  titulo = models.CharField(max_length=200)
  chef = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo
  
class Measure(models.Model):
  valor = models.CharField(max_length=10)

  def __str__(self):
      return self.valor
  

class Ingredient(models.Model):
  nombre = models.CharField(max_length=200)
  cantidad = models.IntegerField()
  medida = models.ForeignKey(Measure, on_delete=models.CASCADE)
  receta = models.ForeignKey(Recipes, on_delete=models.CASCADE)

  def __str__(self):
      return self.nombre
  
class Method(models.Model):
  titulo = models.CharField(max_length=200)
  receta = models.ForeignKey(Recipes, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo
  
class Step(models.Model):
  titulo = models.CharField(max_length=200)
  posicion = models.IntegerField(default=0)
  descripcion = models.TextField(max_length=530)
  tiempo = models.IntegerField()
  preparacion = models.ForeignKey(Method, on_delete=models.CASCADE)

  def __str__(self):
      return self.titulo
  