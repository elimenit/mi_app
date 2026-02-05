"""
Estructura de archivos
.
├── app                  # "app" es un paquete de Python
│   ├── __init__.py      # este archivo hace que "app" sea un "paquete de Python"
│   ├── main.py          # módulo "main", por ejemplo import app.main
│   ├── dependencies.py  # módulo "dependencies", por ejemplo import app.dependencies
│   └── routers          # "routers" es un "subpaquete de Python"
│   │   ├── __init__.py  # hace que "routers" sea un "subpaquete de Python"
│   │   ├── items.py     # submódulo "items", por ejemplo import app.routers.items
│   │   └── users.py     # submódulo "users", por ejemplo import app.routers.users
│   └── internal         # "internal" es un "subpaquete de Python"
│       ├── __init__.py  # hace que "internal" sea un "subpaquete de Python"
│       └── admin.py     # submódulo "admin", por ejemplo import app.internal.admin
"""
# Escalabilidad con APIRouter
"""
Quieres tener las path operations relacionadas con tus 
usuarios separadas del resto del código, para mantenerlo organizado.

Example:
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
"""
# app/dependencias/dependencies.py 
"""
from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
"""
# app/routers/items.py
"""
Digamos que también tienes los endpoints dedicados a manejar "items"
 de tu aplicación en el módulo app/routers/items.py.

Tienes path operations para:

/items/
/items/{item_id}
Es toda la misma estructura que con app/routers/users.py.

Pero queremos ser más inteligentes y simplificar un poco el código.

Sabemos que todas las path operations en este módulo tienen el mismo:

Prefijo de path: /items.
tags: (solo una etiqueta: items).
responses extra.
dependencies: todas necesitan esa dependencia X-Token que creamos.
Entonces, en lugar de agregar todo eso a cada path operation,
 podemos agregarlo al APIRouter
# Example:
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
"""
# Dependecias
"""
Importar las dependencias
Este código vive en el módulo app.routers.items,
 el archivo app/routers/items.py.

Y necesitamos obtener la función de dependencia del módulo 
app.dependencies, el archivo app/dependencies.py.

Así que usamos un import relativo con .. para las dependencias
"""
# Main.py:
"""
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
"""
