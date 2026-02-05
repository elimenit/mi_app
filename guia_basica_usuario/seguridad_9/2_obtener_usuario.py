# Obtener Usuario Actual
"""
En el capítulo anterior, el sistema de seguridad
 (que se basa en el sistema de inyección de dependencias)
 le estaba dando a la path operation function un token como un str:
"""
# Crear un modelo de usuario
"""
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
"""
#Crear una dependencia get_current_user
"""
Vamos a crear una dependencia get_current_user.
¿Recuerdas que las dependencias pueden tener sub-dependencias?
get_current_user tendrá una dependencia con el mismo 
 oauth2_scheme que creamos antes.
De la misma manera que estábamos haciendo antes en la
 path operation directamente, nuestra nueva dependencia 
 get_current_user recibirá un token como
 un str de la sub-dependencia 
# Obtenemos el usuario 
* get_current_user usará una función de utilidad (falsa)
 que creamos, que toma un token como
 un str y devuelve nuestro modelo de Pydantic User:
# inyectamos al usuario actual
* Entonces ahora podemos usar el mismo Depends
 con nuestro get_current_user en la path operation:
###
Entonces ahora podemos usar el mismo Depends
 con nuestro get_current_user en la path operation:
###
"""
# Otros Modelos
"""
Ahora puedes obtener el usuario actual directamente
 en las path operation functions y manejar los mecanismos
 de seguridad a nivel de Dependency Injection, usando Depends.

Y puedes usar cualquier modelo o datos para los requisitos
 de seguridad (en este caso, un modelo de Pydantic User).

Pero no estás limitado a usar algún modelo
 de datos, clase o tipo específico.

¿Quieres tener un id y email y no tener un username
 en tu modelo? Claro. Puedes usar estas mismas herramientas.

¿Quieres solo tener un str? ¿O solo un dict?
 ¿O un instance de clase modelo de base de datos directamente?
 Todo funciona de la misma manera.

¿En realidad no tienes usuarios que inicien sesión
 en tu aplicación sino robots, bots u otros sistemas, que
 solo tienen un token de acceso? Una vez más, todo funciona igual.

Usa cualquier tipo de modelo, cualquier tipo de clase,
 cualquier tipo de base de datos que necesites para tu aplicación.
 FastAPI te cubre con el sistema de inyección de dependencias.
"""
# Tamaño del codigo
"""
Este ejemplo podría parecer extenso. Ten en cuenta que estamos
 mezclando seguridad, modelos de datos, funciones 
 de utilidad y path operations en el mismo archivo.

Pero aquí está el punto clave.

El tema de seguridad e inyección de dependencias se escribe una vez.

Y puedes hacerlo tan complejo como desees. Y aún así,
 tenerlo escrito solo una vez, en un solo lugar. Con toda la flexibilidad.

Pero puedes tener miles de endpoints (path operations)
 usando el mismo sistema de seguridad.

Y todos ellos (o cualquier porción de ellos que quieras)
 pueden aprovechar la reutilización de estas dependencias 
 o cualquier otra dependencia que crees.
"""
# Example
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user