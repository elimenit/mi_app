# ------------- PATH OPERATIONS -------------------#
# Confuguracion del path operation
"""
Ten en cuenta que estos parámetros se pasan directamente
 al path operation decorator, no a tu path operation function.
Example:
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
###
Puedes definir el status_code (HTTP) que se utilizará en el response de tu path operation.

Puedes pasar directamente el código int, como 404.
###
"""
# Tags (Etiquetas)
"""
Puedes añadir tags a tu path operation, pasando el parámetro 
 tags con un list de str (comúnmente solo una str):
 Example:
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
"""
# Tags con Enum
"""
Si tienes una gran aplicación, podrías terminar acumulando varias tags,
 y querrías asegurarte de que siempre uses la misma tag para path operations relacionadas.

En estos casos, podría tener sentido almacenar las tags en un Enum.

FastAPI soporta eso de la misma manera que con strings normales:
# Example
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
"""
# Resumen y Descriptcion
"""
Puedes añadir un summary y description:
# Example
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
"""
# Descripcion desde docstring
"""
Como las descripciones tienden a ser largas y cubrir múltiples líneas,
 puedes declarar la descripción de la path operation en la docstring 
 de la función y FastAPI la leerá desde allí.

Puedes escribir Markdown en el docstring, se interpretará y mostrará
 correctamente (teniendo en cuenta la indentación del docstring)
Example:
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    '''
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    '''
    return item
"""
# Descripcion de Response
"""
Puedes especificar la descripción del response con el parámetro response_description
Example:
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    '''
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    '''
    return item
###
Ten en cuenta que response_description se refiere
 específicamente al response, mientras que description se refiere a la path operation en general.

OpenAPI especifica que cada path operation requiere una descripción de response.

Entonces, si no proporcionas una, FastAPI generará automáticamente una de "Response exitoso".
###
"""
# Deprecar una path operation
"""
Si necesitas marcar una path operation como deprecated, 
 pero sin eliminarla, pasa el parámetro deprecated
# Example
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
"""
# ------------- QUERY PARAMS -------------------#
# ------------- BODY -------------------#
# Uso del parámetro exclude_unset de Pydanti
"""
Si quieres recibir actualizaciones parciales, es muy útil usar
 el parámetro exclude_unset en el .model_dump() del modelo de Pydantic.

Como item.model_dump(exclude_unset=True).

Eso generaría un dict solo con los datos que se establecieron al crear
 el modelo item, excluyendo los valores por defecto.

Luego puedes usar esto para generar un dict solo con los datos que se establecieron
 (enviados en el request), omitiendo los valores por defecto:
# Example
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
"""
# Uso del parámetro update de Pydantic
"""
Ahora, puedes crear una copia del modelo existente
 usando .model_copy(), y pasar el parámetro update 
 con un dict que contenga los datos a actualizar.

Como stored_item_model.model_copy(update=update_data):
"""
