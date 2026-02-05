# Simple OAuth2 con Password y Beare
"""
Vamos a usar las utilidades de seguridad de FastAPI 
 para obtener el username y password.

OAuth2 especifica que cuando se utiliza el "password flow"
 (que estamos usando), el cliente/usuario debe enviar campos
  username y password como form data.

Y la especificación dice que los campos deben llamarse así.
 Por lo que user-name o email no funcionarían.

Pero no te preocupes, puedes mostrarlo como quieras
 a tus usuarios finales en el frontend.

Y tus modelos de base de datos pueden usar
 cualquier otro nombre que desees.

Pero para la path operation de inicio de sesión,
 necesitamos usar estos nombres para ser compatibles
  con la especificación (y poder, por ejemplo, utilizar
   el sistema de documentación integrada de la API).

La especificación también establece que el username
 y password deben enviarse como
 form data (por lo que no hay JSON aquí).
"""
# Scope
"""
La especificación también indica que el cliente 
 puede enviar otro campo del formulario llamado "scope".

El nombre del campo del formulario es scope (en singular),
 pero en realidad es un string largo con "scopes" separados por espacios.

Cada "scope" es simplemente un string (sin espacios).

Normalmente se utilizan para declarar permisos
 de seguridad específicos, por ejemplo:

 * users:read o users:write son ejemplos comunes.
 * instagram_basic es usado por Facebook / Instagram.
 * https://www.googleapis.com/auth/drive es usado por Google.
"""
# Código para obtener el username y password
"""
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

###
OAuth2PasswordRequestForm es una dependencia de clase
 que declara un body de formulario con:

 * El username.
 * El password.
 * Un campo opcional scope como un string grande,
    compuesto por strings separados por espacios.
 * Un grant_type opcional
 * Un client_id opcional (no lo necesitamos para nuestro ejemplo).
 * Un client_secret opcional (no lo necesitamos para nuestro ejemplo).
###
Info:
OAuth2PasswordRequestForm no es una clase especial
 para FastAPI como lo es OAuth2PasswordBearer.

OAuth2PasswordBearer hace que FastAPI sepa que es un
 esquema de seguridad. Así que se añade de esa manera a OpenAPI.

Pero OAuth2PasswordRequestForm es solo una dependencia de clase
 que podrías haber escrito tú mismo, o podrías haber
  declarado parámetros de Form directamente.

Pero como es un caso de uso común, se proporciona
 directamente por FastAPI, solo para facilitarlo
"""
# DEvolver el token
"""
El response del endpoint token debe ser un objeto JSON.

Debe tener un token_type. En nuestro caso, como estamos
 usando tokens "Bearer", el tipo de token debe ser "bearer".

Y debe tener un access_token, con un string que contenga
 nuestro token de acceso.

Para este ejemplo simple, vamos a ser completamente
 inseguros y devolver el mismo username como el token.
"""
# Actualizar dependencias 
"""
Ahora vamos a actualizar nuestras dependencias.

Queremos obtener el current_user solo si este usuario está activo.

Entonces, creamos una dependencia adicional
 get_current_active_user que a su vez utiliza get_current_user como dependencia.

Ambas dependencias solo devolverán un error HTTP
 si el usuario no existe, o si está inactivo.

Así que, en nuestro endpoint, solo obtendremos un usuario
 si el usuario existe, fue autenticado correctamente, y está activo:
"""
## aun es inseguro