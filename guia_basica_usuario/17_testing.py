# TESTING
"""
Gracias a Starlette, escribir pruebas para aplicaciones
 de FastAPI es fácil y agradable.

Está basado en HTTPX, que a su vez está diseñado basado
 en Requests, por lo que es muy familiar e intuitivo.

Con él, puedes usar pytest directamente con FastAPI.
"""
# TestClient (pip install "fastapi[all]")
"""
Importa TestClient.

Crea un TestClient pasándole tu aplicación de FastAPI.

Crea funciones con un nombre que comience
 con test_ (esta es la convención estándar de pytest).

Usa el objeto TestClient de la misma manera que con httpx.

Escribe declaraciones assert simples con las expresiones
 estándar de Python que necesites revisar
 (otra vez, estándar de pytest)
# Example:
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
"""
# OJO
"""
Nota que las funciones de prueba son def normales, no async def.

Y las llamadas al cliente también son llamadas normales, sin usar await.

Esto te permite usar pytest directamente sin complicaciones
###
También podrías usar from starlette.testclient import TestClient.

FastAPI proporciona el mismo starlette.testclient
 como fastapi.testclient solo por conveniencia para ti,
  el desarrollador. Pero proviene directamente de Starlette.
###
"""
# Pruebas
"""
Ahora extiende este ejemplo y añade más detalles
 para ver cómo escribir pruebas para diferentes partes.

Archivo de aplicación FastAPI extendido¶
Continuemos con la misma estructura de archivos que antes:


.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
Digamos que ahora el archivo main.py con tu aplicación
 de FastAPI tiene algunas otras path operations.

Tiene una operación GET que podría devolver un error.

Tiene una operación POST que podría devolver varios errores.

Ambas path operations requieren un X-Token header.
# example:
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item
"""
# Pruebas extendidas
"""
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
###
Por ejemplo:

Para pasar un parámetro de path o query, añádelo a la URL misma.
Para pasar un cuerpo JSON, pasa un objeto de Python (por ejemplo, un dict) al parámetro json.
Si necesitas enviar Form Data en lugar de JSON, usa el parámetro data en su lugar.
Para pasar headers, usa un dict en el parámetro headers.
Para cookies, un dict en el parámetro cookie
###
"""

