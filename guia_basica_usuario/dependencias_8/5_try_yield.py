# DEpendencias con yield
"""
FastAPI admite dependencias que realizan algunos
 pasos adicionales después de finalizar.

Para hacer esto, usa yield en lugar de return,
 y escribe los pasos adicionales (código) después.
"""
# Una dependencia con yield
"""
Por ejemplo, podrías usar esto para crear una sesión
 de base de datos y cerrarla después de finalizar.

Solo el código anterior e incluyendo la declaración
 yield se ejecuta antes de crear un response:
# Example:
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
"""
# Una dependencia con try y yield 
"""
Si usas un bloque try en una dependencia con yield,
 recibirás cualquier excepción que se 
 haya lanzado al usar la dependencia.

Por ejemplo, si algún código en algún punto intermedio,
 en otra dependencia o en una path operation, 
 realiza un "rollback" en una transacción de base 
 de datos o crea cualquier otro error, 
 recibirás la excepción en tu dependencia.

Por lo tanto, puedes buscar esa excepción
 específica dentro de la dependencia con except SomeException.

Del mismo modo, puedes usar finally para asegurarte
 de que los pasos de salida se ejecuten, 
 sin importar si hubo una excepción o no.
"""
# Sub_dependencias con yield
"""
Puedes tener sub-dependencias y "árboles"
 de sub-dependencias de cualquier tamaño 
 y forma, y cualquiera o todas ellas pueden usar yield.

FastAPI se asegurará de que el 
 "código de salida" en cada dependencia 
 con yield se ejecute en el orden correcto.

Por ejemplo, dependency_c puede tener
 una dependencia de dependency_b, 
 y dependency_b de dependency_a:
# Example:
#
from typing import Annotated

from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
#
###
Y todas ellas pueden usar yield.

En este caso, dependency_c, para
 ejecutar su código de salida, necesita que 
 el valor de dependency_b (aquí llamado dep_b) 
 todavía esté disponible.

Y, a su vez, dependency_b necesita que el
 valor de dependency_a (aquí llamado dep_a) 
 esté disponible para su código de salida.
###
De la misma manera, podrías tener algunas 
dependencias con yield y otras dependencias 
con return, y hacer que algunas
 de esas dependan de algunas de las otras.

Y podrías tener una sola dependencia que
 requiera varias otras dependencias con yield, etc.

Puedes tener cualquier combinación de dependencias que quieras.

FastAPI se asegurará de que todo se ejecute en el orden correcto.
"""
# Dependencias con yield y HTTPException
"""
Viste que puedes usar dependencias con yield y tener bloques
 try que intentan ejecutar algo de código y
  luego ejecutar código de salida después de finally.

También puedes usar except para capturar la excepción
 que se lanzó y hacer algo con ella.

Por ejemplo, puedes lanzar una excepción diferente, como HTTPException.
# Example
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item
###
Esta es una técnica algo avanzada, y en la mayoría de los casos
 realmente no la necesitarás, ya que puedes lanzar excepciones 
 (incluyendo HTTPException) desde dentro del resto del 
 código de tu aplicación, por ejemplo, en la path operation function.
"""
# Dependencias con yiueld y except
"""
Si capturas una excepción usando except en una dependencia con yield
 y no la lanzas nuevamente (o lanzas una nueva excepción), 
 FastAPI no podrá notar que hubo una excepción, 
 al igual que sucedería con Python normal:
# Example
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


class InternalError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except InternalError:
        print("Oops, we didn't raise again, Britney 😱")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id
###
EL cliente vera un 500 internal server
###
"""
# Siempre raise en Dependencias con yield y except
"""
Si capturas una excepción en una dependencia con yield,
 a menos que estés lanzando otra HTTPException o similar, 
 deberías volver a lanzar la excepción original.

Puedes volver a lanzar la misma excepción usando raise.
"""
# Salida temprana y scope
"""
Normalmente, el código de salida de las dependencias
 con yield se ejecuta después de que el response se envía al cliente.

Pero si sabes que no necesitarás usar la dependencia
 después de regresar de la path operation function, 
 puedes usar Depends(scope="function") para decirle a FastAPI 
 que debe cerrar la dependencia después de que la path
 operation function regrese, pero antes de que se envíe el response.
# Example:
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_username():
    try:
        yield "Rick"
    finally:
        print("Cleanup up before response is sent")


@app.get("/users/me")
def get_user_me(username: Annotated[str, Depends(get_username, scope="function")]):
    return username
###
* Depends() recibe un parámetro scope que puede ser:

 * "function": iniciar la dependencia antes de la path operation function
     que maneja el request, terminar la dependencia después de que termine
     la path operation function, pero antes de que el response se envíe 
     de vuelta al cliente. Entonces, la función de dependencia 
     se ejecutará alrededor de la path operation function.
 * "request": iniciar la dependencia antes de la path operation function
     que maneja el request (similar a cuando se usa "function"), 
     pero terminar después de que el response se envíe de vuelta al cliente.
     Entonces, la función de dependencia se ejecutará alrededor del 
     request y del ciclo del response.
* Si no se especifica y la dependencia tiene yield, tendrá un scope de "request" por defecto
###
"""
# Context Managers
"""
Los "Context Managers" son aquellos objetos de Python que puedes usar en una declaración with.
# Example
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)

###
Internamente, open("./somefile.txt") crea un objeto llamado "Context Manager".

Cuando el bloque with termina, se asegura de cerrar el archivo, incluso si hubo excepciones.

Cuando creas una dependencia con yield, FastAPI creará internamente un context manager
 para ella y lo combinará con algunas otras herramientas relacionadas.
###
"""
# Crear context Manager
"""
creando una clase con dos métodos: __enter__() y __exit__()
# Example:
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
###
Otra manera de crear un context manager es con:

* @contextlib.contextmanager o
* @contextlib.asynccontextmanager
usándolos para decorar una función con un solo yield.

Eso es lo que FastAPI usa internamente para dependencias con yield.

Pero no tienes que usar los decoradores para las dependencias de FastAPI (y no deberías).

FastAPI lo hará por ti internamente.
"""