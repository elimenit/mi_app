# Dependicias en decoradores de el path-operation
"""
* En algunos casos realmente no necesitas el valor de retorno
   de una dependencia dentro de tu path operation function.
* O la dependencia no devuelve un valor.
* Pero aún necesitas que sea ejecutada/resuelta.
* Para esos casos, en lugar de declarar un parámetro de path
   operation function con Depends, puedes añadir 
   una list de dependencies al decorador de path operation
* El decorador de path operation recibe un argumento opcional dependencies.
* Debe ser una list de Depends():
# Example:
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
###
Algunos editores revisan los parámetros de función no usados y los muestran como errores.

Usando estas dependencies en el decorador de path operation puedes asegurarte de
 que se ejecutan mientras evitas errores en editores/herramientas.
###
"""
# Requisitos dependencia 
"""
* Pueden declarar requisitos de request (como headers) u otras sub-dependencias
"""
# LAmzamiento de exceptciones 
"""
Estas dependencias pueden raise excepciones, igual que las dependencias normales
"""
# Valores de retorno
"""
Y pueden devolver valores o no, los valores no serán usados.
Así que, puedes reutilizar una dependencia normal
 (que devuelve un valor) que ya uses en otro lugar, 
 y aunque el valor no se use, la dependencia será ejecutada:
"""