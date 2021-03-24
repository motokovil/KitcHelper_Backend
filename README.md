# KitcHelper
## Ayudante de Cocina.
Te ayuda a almacenar tus recetas favoritas y los productos que necesitas. Al iniciar una receta, KH consume lo necesario de los productos en la despensa. Si los productos se estan agotando, KH te provee de una lista de compras actualizada, para que asi ahorres tiempo y sepas exactamente lo que necesitas.

## Installation
Crea e inicia un ambiente virtual de python.
Usa pip para instalar el requirements.txt.
Comprueba que el modo debug este en False antes de desplegar.
Realiza las migraciones de las tablas.


## Endpoints
### Api / v1 / Recipes /

```python  

  #Post
  Body = { 
    "titulo" : "titulo de la receta",
    ...
  }
  
  #Patch & Delete
  Body = { 
    "receta" : 1,
    "data": {"titulo": "Pizza"}
  }
  
```
### Api / v1 / Recipes / Execute /
#### Execute
Si la receta tiene ingredientes nuevos que no estan en la despensa o si al validar la despensa los ingredientes no son suficientes para la receta, retorna una lista con lo que hace falta. En caso de que estén los productos disponibles, consumirán lo necesario para realizar la receta proporcionada.

```python
  Body = { 
    "receta" : 1
  }
```

### Api / v1 / Pantry / ShoppingList /
Retorna una lista de compras general de acuerdo a los productos que tienes en la despensa, validando cuales de ellos estan por agotarse.
```python
{
  "multipass": true,
  "detail": "Lista de compra creada",
  "data": [
    {
      "id": 180,
      "titulo": "Tomate",
      "cantidad": 5,
      "precio": 2000,
      "lista": 213,
      "producto": 2
    }
  ]
}
```
### Api / v1 / Pantry / ShoppingList / get /
Es una vista para todas las listas de compras que han sido creadas.
```python
{
  "multipass": true,
  "detail": "Listas de compra",
  "data": [
    {
      "id": 210,
      "titulo": "Nueva lista",
      "descripcion": "Descripcion",
      "activa": true,
      "pantry": 1
    },
    {
      "id": 211,
      "titulo": "Nueva lista",
      "descripcion": "Descripcion",
      "activa": true,
      "pantry": 1
    }
  ]
}
```
