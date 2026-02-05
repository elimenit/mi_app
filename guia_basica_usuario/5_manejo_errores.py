# Manejo de errores
"""
Existen muchas situaciones en las que necesitas notificar
 un error a un cliente que está usando tu API.

Este cliente podría ser un navegador con un frontend,
 un código de otra persona, un dispositivo IoT, etc.

Podrías necesitar decirle al cliente que:
 * El cliente no tiene suficientes privilegios para esa operación.
 * El cliente no tiene acceso a ese recurso.
 * El ítem al que el cliente intentaba acceder no existe.
 * etc
* Para devolver responses HTTP con errores al cliente, usa HTTPException.
# Example:
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
"""
# LAnzar una HTTPException
"""
HTTPException es una excepción de Python normal con datos adicionales relevantes para APIs.

Debido a que es una excepción de Python, no la return, sino que la raise.

Esto también significa que si estás dentro de una función de utilidad
 que estás llamando dentro de tu path operation function, y lanzas
 el HTTPException desde dentro de esa función de utilidad, 
 no se ejecutará el resto del código en la path operation function, 
 terminará ese request de inmediato y enviará el error HTTP del HTTPException al cliente.

El beneficio de lanzar una excepción en lugar de returnar un valor
 será más evidente en la sección sobre Dependencias y Seguridad.

En este ejemplo, cuando el cliente solicita un ítem por un ID que no existe,
 lanza una excepción con un código de estado de 404:
# Example:
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
"""
# Agregar headers personalizados
"""
Existen algunas situaciones en las que es útil poder agregar
 headers personalizados al error HTTP. 
 Por ejemplo, para algunos tipos de seguridad.

Probablemente no necesitarás usarlos directamente en tu código.

Pero en caso de que los necesites para un escenario avanzado,
 puedes agregar headers personalizados:
# Example:

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

"""
# Gestionar exceptciones Personalizadas
"""
Puedes agregar manejadores de excepciones personalizados
 con las mismas utilidades de excepciones de Starlette.

Supongamos que tienes una excepción personalizada
 UnicornException que tú (o un paquete que usas) podrías lanzar.

Y quieres manejar esta excepción globalmente con FastAPI.

Podrías agregar un manejador de excepciones
 personalizado con @app.exception_handler():
# Example:
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
###
Aquí, si solicitas /unicorns/yolo, la path operation lanzará un UnicornException.

Pero será manejado por el unicorn_exception_handler.

Así que recibirás un error limpio, con un código de estado HTTP
 de 418 y un contenido JSON de:
"""
# Sobrescribir los manejadores de excepciones predeterminados
"""
FastAPI tiene algunos manejadores de excepciones predeterminados.

Estos manejadores se encargan de devolver los responses JSON
 predeterminadas cuando lanzas un HTTPException y cuando
 el request tiene datos inválidos.

Puedes sobrescribir estos manejadores de excepciones con los tuyos propios.
"""
# Sobrescribir excepciones de validación de request
"""
Cuando un request contiene datos inválidos,
 FastAPI lanza internamente un RequestValidationError.
Y también incluye un manejador de excepciones predeterminado para ello.
Para sobrescribirlo, importa el RequestValidationError
 y úsalo con @app.exception_handler(RequestValidationError)
  para decorar el manejador de excepciones.
El manejador de excepciones recibirá un Request y la excepción
# Example (Mucho time)
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
###
También podrías usar from starlette.responses import PlainTextResponse.

FastAPI ofrece las mismas starlette.responses como
 fastapi.responses solo como una conveniencia para ti,
 el desarrollador. Pero la mayoría de los responses disponibles 
 vienen directamente de Starlette.
"""
######## ADVERTENCIA ##########
#--------#######------#########
"""
Ten en cuenta que RequestValidationError contiene
 la información del nombre de archivo y la línea donde ocurre el 
 error de validación, para que puedas mostrarla en tus logs con 
 la información relevante si quieres.

Pero eso significa que si simplemente lo conviertes a un string
 y devuelves esa información directamente, podrías estar 
 filtrando un poquito de información sobre tu sistema, 
 por eso aquí el código extrae y muestra cada error de forma independiente.
"""
#--------#######------#########
# Usar el body de RequestValidationError
"""
El RequestValidationError contiene el body que recibió con datos inválidos.

Podrías usarlo mientras desarrollas tu aplicación
 para registrar el body y depurarlo, devolverlo al usuario, etc
# Example:
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item

"""
# HTTPException de FastAPI vs HTTPException de Starlette
"""
FastAPI tiene su propio HTTPException.

Y la clase de error HTTPException de FastAPI hereda
 de la clase de error HTTPException de Starlette.

La única diferencia es que el HTTPException de FastAPI
 acepta cualquier dato JSON-able para el campo detail, 
 mientras que el HTTPException de Starlette solo acepta strings para ello.

Así que puedes seguir lanzando un HTTPException de FastAPI como de costumbre en tu código.

Pero cuando registras un manejador de excepciones, deberías registrarlo
 para el HTTPException de Starlette.

De esta manera, si alguna parte del código interno de Starlette,
 o una extensión o plug-in de Starlette, lanza un HTTPException 
 de Starlette, tu manejador podrá capturarlo y manejarlo.

En este ejemplo, para poder tener ambos HTTPException en el mismo código,
 las excepciones de Starlette son renombradas a StarletteHTTPException:
# Example
from starlette.exceptions import HTTPException as StarletteHTTPException
"""
# Reutilizar los manejadores de excepciones de FastAPI
"""
Si quieres usar la excepción junto con los mismos manejadores de excepciones
 predeterminados de FastAPI, puedes importar y reutilizar los manejadores
  de excepciones predeterminados de fastapi.exception_handlers
# Example
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
###
En este ejemplo solo estás printeando el error
 con un mensaje muy expresivo, pero te haces una idea.
 Puedes usar la excepción y luego simplemente reutilizar
 los manejadores de excepciones predeterminados.
###
"""