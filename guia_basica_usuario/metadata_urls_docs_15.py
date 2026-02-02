# Metadata para la API
"""
Puedes establecer los siguientes campos que se usan
 en la especificación OpenAPI y en las interfaces
  automáticas de documentación de la API:

Parámetro |	        Tipo	Descripción
title	            str	     El título de la API.
summary	            str	     Un resumen corto de la API. Disponible desde OpenAPI 3.1.0, FastAPI 0.99.0.
description	        str	     Una breve descripción de la API. Puede usar Markdown.
version	            string	La versión de la API. Esta es la versión de tu propia aplicación, no de OpenAPI. Por ejemplo, 2.5.0.
terms_of_service	str	     Una URL a los Términos de Servicio para la API. Si se proporciona, debe ser una URL.
contact	            dict	La información de contacto para la API expuesta. Puede contener varios campos.
license_info	    dict	La información de la licencia para la API expuesta. Puede contener varios campos.
"""
# Configuracion
"""
from fastapi import FastAPI

description = '''
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
'''

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
"""
# Metadata para Etiquetas
"""
También puedes agregar metadata adicional para las
 diferentes etiquetas usadas para agrupar tus path
  operations con el parámetro openapi_tags.

Este toma una list que contiene un diccionario para cada etiqueta.

Cada diccionario puede contener:

name (requerido): un str con el mismo nombre de
 etiqueta que usas en el parámetro tags en tus
  path operations y APIRouters.
description: un str con una breve descripción de
 la etiqueta. Puede tener Markdown y se mostrará
  en la interfaz de documentación.
externalDocs: un dict que describe documentación externa con:
description: un str con una breve descripción para la documentación externa.
url (requerido): un str con la URL para la documentación externa.

Example:
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
"""
# Orden de las etiquetas (tags)
"""
El orden de cada diccionario de metadata de etiqueta también
 define el orden mostrado en la interfaz de documentación.

Por ejemplo, aunque users iría después de items en orden
 alfabético, se muestra antes porque agregamos su metadata
  como el primer diccionario en la list.
"""
# URL para OpenApi
"""
Por defecto, el esquema OpenAPI se sirve en /openapi.json.

Pero puedes configurarlo con el parámetro openapi_url.

Por ejemplo, para configurarlo para que se sirva en /api/v1/openapi.json:
# Example:
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
###
Si quieres deshabilitar el esquema OpenAPI completamente,
 puedes establecer openapi_url=None, eso también deshabilitará
  las interfaces de usuario de documentación que lo usan.
###
"""
# URL para DOCS
"""
Puedes configurar las dos interfaces de usuario de documentación incluidas:

Swagger UI: servida en /docs.
Puedes establecer su URL con el parámetro docs_url.
Puedes deshabilitarla estableciendo docs_url=None.
ReDoc: servida en /redoc.
Puedes establecer su URL con el parámetro redoc_url.
Puedes deshabilitarla estableciendo redoc_url=None.
Por ejemplo, para configurar Swagger UI para que se
 sirva en /documentation y deshabilitar ReDoc:

# Example:
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
"""