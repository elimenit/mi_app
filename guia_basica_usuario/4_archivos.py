# Archivos
"""
Para recibir archivos subidos, primero instala python-multipart
Esto es porque los archivos subidos se envían como "form data".
# Example:
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
###
Los archivos se subirán como "form data".

Si declaras el tipo de tu parámetro de path
 operation function como bytes, FastAPI
  leerá el archivo por ti y recibirás el contenido como bytes.

Ten en cuenta que esto significa que todo el
 contenido se almacenará en memoria.
  Esto funcionará bien para archivos pequeños.

Pero hay varios casos en los que podrías beneficiarte de usar UploadFile.
"""
# Parametros de archivo con UploadFile
"""
UploadFile tiene los siguientes atributos:

filename: Un str con el nombre original del archivo
    que fue subido (por ejemplo, myimage.jpg).
content_type: Un str con el tipo de contenido 
    (MIME type / media type) (por ejemplo, image/jpeg).
file: Un SpooledTemporaryFile (un objeto parecido a un archivo). 
    Este es el objeto de archivo Python real que puedes pasar
    directamente a otras funciones o paquetes
    que esperan un objeto "parecido a un archivo".
UploadFile tiene los siguientes métodos async.
 Todos ellos llaman a los métodos correspondientes
  del archivo por debajo (usando el SpooledTemporaryFile interno).

* write(data): Escribe data (str o bytes) en el archivo.
* read(size): Lee size (int) bytes/caracteres del archivo.
* seek(offset): Va a la posición de bytes offset (int) en el archivo.
Por ejemplo, await myfile.seek(0) iría al inicio del archivo.
 Esto es especialmente útil si ejecutas await myfile.read() una vez
 y luego necesitas leer el contenido nuevamente.
* close(): Cierra el archivo.
# Example
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
###
Como todos estos métodos son métodos
 async, necesitas "await" para ellos.

Por ejemplo, dentro de una path operation
 function async puedes obtener los contenidos con:

contents = await myfile.read()

Si estás dentro de una path operation function
 normal def, puedes acceder al UploadFile.file directamente, por ejemplo:

contents = myfile.file.read()
###
"""
# UploadFile vs File
"""
Usar UploadFile tiene varias ventajas sobre bytes:

* No tienes que usar File() en el valor por defecto del parámetro.
* Usa un archivo "spooled":
* Un archivo almacenado en memoria hasta un límite
 de tamaño máximo, y después de
 superar este límite, se almacenará en el disco.
* Esto significa que funcionará bien para archivos grandes
 como imágenes, videos, binarios grandes, 
 etc. sin consumir toda la memoria.
* Puedes obtener metadatos del archivo subido.
* Tiene una interfaz async parecida a un archivo.
* Expone un objeto Python real SpooledTemporaryFile que
 puedes pasar directamente a otros paquetes 
 que esperan un objeto parecido a un archivo.
"""
# Formularios o Qué es "Form Data"
"""
La manera en que los forms de HTML (<form></form>) 
 envían los datos al servidor normalmente
 utiliza una codificación "especial"
 para esos datos, es diferente de JSON.
###
Los datos de los forms normalmente se codifican usando el
 "media type" application/x-www-form-urlencoded cuando no incluyen archivos.

Pero cuando el formulario incluye archivos, se codifica
 como multipart/form-data. Si usas File, FastAPI
  sabrá que tiene que obtener los archivos de la parte correcta del cuerpo.

Si deseas leer más sobre estas codificaciones y
 campos de formularios, dirígete a la MDN web docs para POST.(https://developer.mozilla.org/es-US/docs/Web/HTTP/Reference/Methods/POST)
###
"""
# Subida opcional de archivos
"""
Puedes hacer un archivo opcional utilizando anotaciones 
 de tipos estándar y estableciendo un valor por defecto de None:
# Example:
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}

"""
# UploadFile con Metadatos Adicionales
"""
También puedes usar File() con UploadFile,
 por ejemplo, para establecer metadatos adicionales:
Example: 
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename} 
"""
# Subida de Multiples archivos
"""
Es posible subir varios archivos al mismo tiempo.

Estarían asociados al mismo "campo de formulario" enviado usando "form data".

Para usar eso, declara una lista de bytes o UploadFile
# Example
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = '''
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    '''
    return HTMLResponse(content=content)
"""
# Subida de multiples Archivos con metadatos adicionales
"""
Y de la misma manera que antes, puedes usar File()
 para establecer parámetros adicionales, incluso para UploadFile:
# Example:
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = '''
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    '''
    return HTMLResponse(content=content)
"""
# Sugerencia
"""
Usa File, bytes y UploadFile para declarar archivos
 que se subirán en el request, enviados como form data.
"""
# Formularios y archivos del Request ()
# Example
# Cuandpo envias un cv
"""
Para recibir archivos subidos y/o form data, primero instala python-multipart.
Asegúrate de crear un entorno virtual, actívalo y luego instálalo, por ejemplo:
# example of Installation
$ pip install python-multipart
# Example:
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
"""
# Definir File y Form
"""
Crea parámetros de archivo y formulario de la misma manera que lo harías para Body o Query
###
Los archivos y campos de formulario se subirán
 como form data y recibirás los archivos y campos de formulario.
Usa File y Form juntos cuando necesites recibir datos y archivos en el mismo request.
###
"""

### ---------ADVERTENCIA----------###
#####-------#####------#####
"""
Puedes declarar múltiples parámetros File y Form en una path operation,
 pero no puedes también declarar campos Body que esperas recibir como JSON,
 ya que el request tendrá el body codificado
 usando multipart/form-data en lugar de application/json.

Esto no es una limitación de FastAPI, es parte del protocolo HTTP.
"""
#####-------#####------#####
