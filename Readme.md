# API (Aplicattion Programing Interface)
Todos los endpoints devolveran la entidad que esta manejando

## Objetivo 
* Leer mails o mensajes de  WhatsApps

* Clasifica automáticamente:

    * reclamo

    * consulta

    * urgencia

* Genera:

    * respuesta borrador

    * ticket interno

* resumen semanal automático

# Users

## GET /api/users/1
[
    {
        "name": "Jhon",
        "lastname": "Doe",
        "age":21
    },
    ...
]

## POST /api/users
{
    "name": "nombre",
    "lastname": "apellido",
    "email": "correo",
    "password": "contrasena"
}

## PUT /api/users/
{
    "user_id": 1
    "name": "nombre",
    "lastname": "apellido",
    "password": "contrasena"
}

## DELETE /api/users/{id}
{
    "password": "contrasenia"
}

# Admin
administra los usuarios

## GET /api/admin
[
    {
        "user_id": 1
        "name": "Jhon",
        "lastname": "Doe",
        "email": "correo",
        "password":"contrasena"
    },
    ...
]

# Wattsap
Los mensajes de Wattsap

## GET /api/users/<id>/
Aqui nos deberia mostrar los wattsapp

# BUENAS PRACTICAS
## En resumen, para aplicar actualizaciones parciales deberías:
* (Opcionalmente) usar PATCH en lugar de PUT.
* Recuperar los datos almacenados.
* Poner esos datos en un modelo de Pydantic.
* Generar un dict sin valores por defecto del modelo de entrada (usando exclude_unset).
   De esta manera puedes actualizar solo los valores realmente establecidos por el usuario,
   en lugar de sobrescribir valores ya almacenados con valores por defecto en tu modelo.
* Crear una copia del modelo almacenado, actualizando sus atributos con las actualizacione
   s parciales recibidas (usando el parámetro update).
* Convertir el modelo copiado en algo que pueda almacenarse
   en tu DB (por ejemplo, usando el jsonable_encoder).
    Esto es comparable a usar el método .model_dump() del modelo de nuevo,
    pero asegura (y convierte) los valores a tipos de datos que pueden 
    convertirse a JSON, por ejemplo, datetime a str.
* Guardar los datos en tu DB.
* Devolver el modelo actualizado 