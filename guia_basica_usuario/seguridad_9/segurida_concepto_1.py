# Concepto de autenticacion
"""
Imaginemos que tienes tu API de backend en algún dominio.

Y tienes un frontend en otro dominio o en un path diferente
 del mismo dominio (o en una aplicación móvil).

Y quieres tener una forma para que el frontend se autentique
 con el backend, usando un username y password.

Podemos usar OAuth2 para construir eso con FastAPI.

Pero vamos a ahorrarte el tiempo de leer la larga
 especificación completa solo para encontrar
 esos pequeños fragmentos de información que necesitas.

Usemos las herramientas proporcionadas
 por FastAPI para manejar la seguridad.
Example:
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
### Ejecutar:
El paquete python-multipart se instala automáticamente con FastAPI
 cuando ejecutas el comando pip install "fastapi[standard]".

Sin embargo, si usas el comando pip install fastapi,
 el paquete python-multipart no se incluye por defecto.

Para instalarlo manualmente, asegúrate de crear un entorno virtual,
 activarlo, y luego instalarlo con:

$ pip install python-multipart

Esto se debe a que OAuth2 utiliza "form data"
 para enviar el username y password.
###
"""
# Flujo del Password
"""
Ahora retrocedamos un poco y entendamos qué es todo eso.

El "flujo" password es una de las formas ("flujos")
 definidas en OAuth2, para manejar la seguridad y la autenticación.

OAuth2 fue diseñado para que el backend o la API pudieran
 ser independientes del servidor que autentica al usuario.

Pero en este caso, la misma aplicación de FastAPI
 manejará la API y la autenticación.

Así que, revisémoslo desde ese punto de vista simplificado:
* El usuario escribe el username y password
 en el frontend, y presiona Enter.

 * El frontend (ejecutándose en el navegador del usuario)
    envía ese username y password a una URL específica en
    nuestra API (declarada con tokenUrl="token").
 * La API verifica ese username y password, y responde
    con un "token" (no hemos implementado nada de esto aún).
 * Un "token" es solo un string con algún contenido que
    podemos usar luego para verificar a este usuario.
    * Normalmente, un token se establece para que expire
       después de algún tiempo.
    * Así que, el usuario tendrá que volver a iniciar
       sesión más adelante.
    * Y si el token es robado, el riesgo es menor.
       No es como una llave permanente que funcionará
        para siempre (en la mayoría de los casos).
* El frontend almacena temporalmente ese token en algún lugar.
* El usuario hace clic en el frontend para
   ir a otra sección de la aplicación web frontend.
* El frontend necesita obtener más datos de la API.
 * Pero necesita autenticación para ese endpoint específico.
 * Así que, para autenticarse con nuestra API, envía un header
    Authorization con un valor de Bearer más el token.
 * Si el token contiene foobar, el contenido del header
    Authorization sería: Bearer foobar.
"""
# 2PasswordBearer de FastAPI
"""
FastAPI proporciona varias herramientas,
 en diferentes niveles de abstracción, para implementar
  estas funcionalidades de seguridad.

En este ejemplo vamos a usar OAuth2, con el flujo Password,
 usando un token Bearer. Hacemos eso utilizando
 la clase OAuth2PasswordBearer.
### 
Un token "bearer" no es la única opción.
Pero es la mejor para nuestro caso de uso.
Y podría ser la mejor para la mayoría de los casos de uso,
 a menos que seas un experto en OAuth2 y sepas exactamente
 por qué hay otra opción que se adapta mejor a tus necesidades.

En ese caso, FastAPI también te proporciona
 las herramientas para construirlo.
###
Cuando creamos una instance de la clase OAuth2PasswordBearer
 pasamos el parámetro tokenUrl. Este parámetro contiene la
 URL que el cliente (el frontend corriendo en el navegador
 del usuario) usará para enviar el username y password
 a fin de obtener un token.
# Example:
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
###
Aquí tokenUrl="token" se refiere a una URL relativa
 token que aún no hemos creado. Como es una URL relativa,
 es equivalente a ./token.

Porque estamos usando una URL relativa, si tu API
 estuviera ubicada en https://example.com/, entonces
 se referiría a https://example.com/token. Pero si tu 
 API estuviera ubicada en https://example.com/api/v1/,
 entonces se referiría a https://example.com/api/v1/token.

Usar una URL relativa es importante para asegurarse de que
 tu aplicación siga funcionando incluso
 en un caso de uso avanzado como Detrás de un Proxy.
###
La variable oauth2_scheme es una instance
 de OAuth2PasswordBearer, pero también es un "callable".
Podría ser llamada como:
    oauth2_scheme(some, parameters)
Así que, puede usarse con Depends
Esta dependencia proporcionará un str que se
 asigna al parámetro token de la path operation function.
###
FastAPI sabrá que puede usar esta dependencia para definir
 un "security scheme" en el esquema
 OpenAPI (y en los docs automáticos del API).
###
"""
# Lo que hace
"""
* Irá y buscará en el request ese header Authorization,
 verificará si el valor es Bearer más algún token,
 y devolverá el token como un str.

* Si no ve un header Authorization, o el valor
   no tiene un token Bearer, responderá directamente
   con un error de código de estado 401 (UNAUTHORIZED).

* Ni siquiera tienes que verificar si el token existe
   para devolver un error. Puedes estar seguro de
   que si tu función se ejecuta, tendrá un str en ese token
"""
