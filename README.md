# KitcHelper
## Ayudante de Cocina.
Te ayuda a almacenar tus recetas favoritas y los productos que necesitas. Al iniciar una receta, KH consume lo necesario de los productos en la despensa. Si los productos se estan agotando, KH te provee de una lista de compras actualizada, para que asi ahorres tiempo y sepas exactamente lo que necesitas.

## Installation
Crea e inicia un ambiente virtual de python.
Usa pip para instalar el requirements.txt.
Comprueba que el modo debug este en False antes de desplegar.
Realiza las migraciones de las tablas.


## Endpoints
Se emplea el metodo POST para la mayoria de solicitudes.

### Api / v1 / Recipes / get, post, patch, delete /

```python
  #Get
  Body = { "token" : jsonwebtoken }
  
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
