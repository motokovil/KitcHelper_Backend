# KitcHelper
## Ayudante de Cocina.
Te ayuda a almacenar tus recetas favoritas y los productos que necesitas. Al iniciar una receta, KH consume lo necesario de los productos en la despensa. Si los productos se estan agotando, KH te provee de una lista de compras actualizada, para asi ahorrar tiempo y sepas exactamente lo que necesitas.

## Installation
Usa pip para instalar el requirements.txt

## Endpoints
Se emplea el metodo POST para la mayoria de solicitudes.

### Api / v1 / Recipes / get, post, patch, delete /

Para gestionar las recetas y la mayoria de apps en los endpoints publicos, se toma como referencia el "user_id" codificado en el token de autenticación.

```python
  #Get
  Body = { "token" : jsonwebtoken }
  
  #Post
  Body = { 
    "token" : jsonwebtoken,
    "titulo" : "titulo de la receta",
  }
  
  #Patch & Delete
  Body = { 
    "token" : jsonwebtoken,
    "receta" : 1,
    ...
  }
  
```
### Api / v1 / Recipes /
#### Validate
Si la receta tiene ingredientes nuevos que no estan en la despensa, retorna una lista con todos ellos. Por otro lado si al validar la despensa los ingredientes no son suficientes para la receta, retorna una lista con lo que hace falta.

```python
  # api/v1/Recipes/validate/
  Body = { 
    "token" : jsonwebtoken,
    "receta" : 1
  }
```
