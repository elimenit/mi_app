# Dependencias Globales
"""
* Para algunos tipos de aplicaciones, podrías querer agregar
   dependencias a toda la aplicación.

* Similar a como puedes agregar dependencies a los path operation
   decorators, puedes agregarlos a la aplicación de FastAPI.

* En ese caso, se aplicarán a todas las path operations en la aplicación
# Example
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
"""
# dependencias en un grupo de path operation
"""
Más adelante, al leer sobre cómo estructurar aplicaciones más grandes
 (Aplicaciones Más Grandes - Múltiples Archivos), posiblemente
 con múltiples archivos, aprenderás cómo declarar un solo 
 parámetro de dependencies para un grupo de path operations.
"""