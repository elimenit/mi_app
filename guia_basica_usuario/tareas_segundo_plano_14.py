
# TAreas en segundo Plano
"""
Puedes definir tareas en segundo plano para que se ejecuten
 después de devolver un response.

Esto es útil para operaciones que necesitan ocurrir 
 después de un request, pero para las que el cliente 
 realmente no necesita esperar a que la operación 
 termine antes de recibir el response.

Esto incluye, por ejemplo:

Notificaciones por email enviadas después
 de realizar una acción:
Como conectarse a un servidor de email y enviar un email 
 tiende a ser "lento" (varios segundos), puedes devolver 
 el response de inmediato y enviar la notificación por 
 email en segundo plano.
Procesamiento de datos:
Por ejemplo, supongamos que recibes un archivo que debe 
 pasar por un proceso lento, puedes devolver un response
 de "Accepted" (HTTP 202) y procesar el archivo en 
 segundo plano.
"""
# Usando BackgroundTasks
"""
Primero, importa BackgroundTasks y define un parámetro
 en tu path operation function con una declaración 
 de tipo de BackgroundTasks:
 # Example:
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
"""
# Crear una funcion de tarea 
"""
Crea una función para que se ejecute como la tarea en segundo plano.

Es solo una función estándar que puede recibir parámetros.

Puede ser una función async def o una función normal def, FastAPI sabrá cómo manejarla correctamente.

En este caso, la función de tarea escribirá en un archivo (simulando el envío de un email).

Y como la operación de escritura no usa async y await, definimos la función con un def normal:
# Example:
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
"""
# Agregar la tarea a segundo plano
"""
Dentro de tu path operation function, pasa tu función 
de tarea al objeto de background tasks con el método .add_task():

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
###
.add_task() recibe como argumentos:

Una función de tarea para ejecutar en segundo plano (write_notification).
Cualquier secuencia de argumentos que deba pasarse a la 
 función de tarea en orden (email).
Cualquier argumento de palabras clave que deba pasarse a la
 función de tarea (message="some notification").
###
"""
# Inyeccion de dependencias
"""
Usar BackgroundTasks también funciona con el sistema de inyección de dependencias,
 puedes declarar un parámetro de tipo BackgroundTasks en varios niveles: 
 en una path operation function, en una dependencia (dependable), 
 en una sub-dependencia, etc.

FastAPI sabe qué hacer en cada caso y cómo reutilizar el mismo 
objeto, de modo que todas las tareas en segundo plano se combinan 
y ejecutan en segundo plano después:
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
"""
# OJO
"""
Si necesitas realizar una computación intensa en segundo plano 
 y no necesariamente necesitas que se ejecute por el mismo 
 proceso (por ejemplo, no necesitas compartir memoria, 
 variables, etc.), podrías beneficiarte del uso de otras
  herramientas más grandes como Celery.

Tienden a requerir configuraciones más complejas,
 un gestor de cola de mensajes/trabajos, como RabbitMQ
  o Redis, pero te permiten ejecutar tareas en segundo
   plano en múltiples procesos, y especialmente, en múltiples servidores.

Pero si necesitas acceder a variables y objetos de la
 misma app de FastAPI, o necesitas realizar pequeñas
  tareas en segundo plano (como enviar una notificación por email),
   simplemente puedes usar BackgroundTasks.
"""
# Resumen
"""
Importa y usa BackgroundTasks con parámetros en path operation functions
 y dependencias para agregar tareas en segundo plan
"""