# Inyecciion de dependencias
"""
En un ejemplo Anterior:
devolviamos un dict como dependencia
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
"""
# Qué hace a una dependencia
"""
Hasta ahora has visto dependencias declaradas como funciones.
Pero esa no es la única forma de declarar dependencias
 (aunque probablemente sea la más común).

El factor clave es que una dependencia debe ser un "callable".

Un "callable" en Python es cualquier cosa que
 Python pueda "llamar" como una función.

Entonces, si tienes un objeto something
 (que podría no ser una función) y puedes "llamarlo" (ejecutarlo) como:
"""
# Clases como dependencia
"""
Puedes notar que para crear una instance de una clase en Python, utilizas esa misma sintaxis.

Por ejemplo:


class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
En este caso, fluffy es una instance de la clase Cat.

Y para crear fluffy, estás "llamando" a Cat.

Entonces, una clase en Python también es un callable.

Entonces, en FastAPI, podrías usar una clase de Python como una dependencia.

Lo que FastAPI realmente comprueba es que sea un
 "callable" (función, clase o cualquier otra cosa) y los parámetros definidos

Si pasas un "callable" como dependencia en FastAPI,
 analizará los parámetros de ese "callable", y
  los procesará de la misma manera que los parámetros
   de una path operation function. Incluyendo sub-dependencias.

Eso también se aplica a los callables sin parámetros.
 Igual que sería para path operation functions sin parámetros.

Entonces, podemos cambiar la dependencia "dependable"
 common_parameters de arriba a la clase CommonQueryParams:

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
"""
### Anotación de tipos vs Depends
"""
Nota cómo escribimos CommonQueryParams dos veces en el código anterior:
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
El último CommonQueryParams, en:

... Depends(CommonQueryParams)

es lo que FastAPI utilizará realmente para saber cuál es la dependencia.

Es a partir de este que FastAPI extraerá los parámetros
 declarados y es lo que FastAPI realmente llamar
"""
