# OAuth2 con Password (y hashing), Bearer con tokens JWT
"""
Ahora que tenemos todo el flujo de seguridad,
 hagamos que la aplicación sea realmente segura,
  usando tokens JWT y hashing de contraseñas seguras.

Este código es algo que puedes usar realmente
 en tu aplicación, guardar los hashes de las
  contraseñas en tu base de datos, etc.

Vamos a empezar desde donde lo dejamos en el
 capítulo anterior e incrementarlo
"""
# Acerca de JWT (Json Web Tokens)
"""
Es un estándar para codificar un objeto JSON en un string largo y denso sin espacios.
No está encriptado, por lo que cualquiera podría recuperar la información de los contenidos.

Pero está firmado. Así que, cuando recibes un token
 que has emitido, puedes verificar que realmente lo emitiste.

De esta manera, puedes crear un token con una expiración de, 
 digamos, 1 semana. Y luego, cuando el usuario regresa al día siguiente
  con el token, sabes que el usuario todavía está registrado en tu sistema.

Después de una semana, el token estará expirado y el usuario no estará
 autorizado y tendrá que iniciar sesión nuevamente para obtener un nuevo token.
  Y si el usuario (o un tercero) intenta modificar el token para cambiar
 la expiración, podrás descubrirlo, porque las firmas no coincidirían.
"""
# Instalar PyJWT
"""
Necesitamos instalar PyJWT para generar y verificar los tokens JWT en Python.
 <!-- pip install pyjwt -->
###
Si planeas usar algoritmos de firma digital como RSA o ECDSA,
 deberías instalar la dependencia del paquete de criptografía pyjwt[crypto].
###
"""
# HAshing de Contraseñas
"""
"Hacer hashing" significa convertir algún contenido (una contraseña en este caso)
 en una secuencia de bytes (solo un string) que parece un galimatías
###
Por qué usar hashing de contraseñas¶
Si tu base de datos es robada, el ladrón no tendrá las contraseñas
 en texto claro de tus usuarios, solo los hashes.

Por lo tanto, el ladrón no podrá intentar usar esa contraseña
 en otro sistema (como muchos usuarios usan la misma contraseña
  en todas partes, esto sería peligroso).
"""
## instalar pwdlib (hashlib ???)
"""
pwdlib es un gran paquete de Python para manejar hashes de contraseñas.

Soporta muchos algoritmos de hashing seguros y utilidades para trabajar con ellos.

El algoritmo recomendado es "Argon2".
    <!-- pip install "pwdlib[argon2]" -->
###
pwdlib también soporta el algoritmo de hashing bcrypt 
pero no incluye algoritmos legacy; para trabajar con hashes
 desactualizados, se recomienda usar el paquete passlib.

Por ejemplo, podrías usarlo para leer y verificar contraseñas
 generadas por otro sistema (como Django) pero hacer hash de cualquier
  contraseña nueva con un algoritmo diferente como Argon2 o Bcrypt.

Y ser compatible con todos ellos al mismo tiempo.
###
Example:
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
"""
# Manejo de tokens JWT
"""
Crea una clave secreta aleatoria que se usará para firmar los tokens JWT
  < -- openssl rand -hex 32 --> -> generara una secuencia de cadenas
Y copia el resultado a la variable SECRET_KEY (no uses la del ejemplo).

Crea una variable ALGORITHM con el algoritmo usado para firmar
 el token JWT y configúralo a "HS256".

Crea una variable para la expiración del token.

Define un Modelo de Pydantic que se usará en el endpoint de
 token para el response.

Crea una función de utilidad para generar un nuevo token de acceso.
Example:
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
###
Actualiza get_current_user para recibir el mismo token que
 antes, pero esta vez, usando tokens JWT.
Decodifica el token recibido, verifícalo y devuelve el usuario actual.
Si el token es inválido, devuelve un error HTTP de inmediat
--
Crea un timedelta con el tiempo de expiración del token.
Crea un verdadero token de acceso JWT y devuélvelo.
-- 
La especificación de JWT dice que hay una clave sub, con el sujeto del token.

Es opcional usarlo, pero ahí es donde pondrías la identificación del usuario,
 por lo que lo estamos usando aquí.

JWT podría ser usado para otras cosas aparte de identificar
 un usuario y permitirle realizar operaciones directamente en tu API.

Por ejemplo, podrías identificar un "coche" o un "artículo de blog".

Luego, podrías agregar permisos sobre esa entidad, como "conducir"
 (para el coche) o "editar" (para el blog).

Y luego, podrías darle ese token JWT a un usuario (o bot), y ellos
 podrían usarlo para realizar esas acciones (conducir el coche,
  o editar el artículo del blog) sin siquiera necesitar tener una
   cuenta, solo con el token JWT que tu API generó para eso.

Usando estas ideas, JWT puede ser utilizado para escenarios mucho más sofisticados.

En esos casos, varias de esas entidades podrían tener el mismo ID,
 digamos foo (un usuario foo, un coche foo, y un artículo del blog foo).

Entonces, para evitar colisiones de ID, cuando crees el token JWT
 para el usuario, podrías prefijar el valor de la clave sub,
  por ejemplo, con username:. Así, en este ejemplo, el valor
   de sub podría haber sido: username:johndoe.

Lo importante a tener en cuenta es que la clave sub debería
 tener un identificador único a lo largo de toda la aplicación,
 y debería ser un string.
"""
# Uso avanzado con scopes
"""
OAuth2 tiene la noción de "scopes".

Puedes usarlos para agregar un conjunto específico de permisos a un token JWT.

Luego, puedes darle este token directamente a un
 usuario o a un tercero, para interactuar con tu API con un conjunto de restricciones.

Puedes aprender cómo usarlos y cómo están integrados
 en FastAPI más adelante en la Guía de Usuario Avanzada
"""




