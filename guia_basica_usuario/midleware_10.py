# Middleware
"""
Puedes añadir middleware a las aplicaciones de FastAPI.
Un "middleware" es una función que trabaja con cada
 request antes de que sea procesada por 
  path operation específica. Y también con cada
   response antes de devolverla.

* Toma cada request que llega a tu aplicación.
* Puede entonces hacer algo a esa request o ejecutar
   cualquier código necesario.
* Luego pasa la request para que sea procesada
   por el resto de la aplicación (por
    alguna path operation).
* Después toma la response generada por la aplicación
 (por alguna path operation).
* Puede hacer algo a esa response o ejecutar
 cualquier código necesario.
* Luego devuelve la response.
###
Si tienes dependencias con yield, el código de
 salida se ejecutará después del middleware.

Si hubiera tareas en segundo plano (cubiertas en la
 sección Tareas en segundo plano, lo verás más adelante),
  se ejecutarán después de todo el middleware.
###
"""
#CREAR un Middleware
"""
Para crear un middleware usas el decorador
 @app.middleware("http") encima de una función.

* La función middleware recibe:
 * La request.
 * Una función call_next que recibirá la request como parámetro.
  * Esta función pasará la request a la
     correspondiente path operation.
  * Luego devuelve la response generada por la
     correspondiente path operation.
* Puedes entonces modificar aún más la response antes de devolverla.
# Example:
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
"""
# Antes y Despues de la Response
"""
Puedes añadir código que se ejecute con la request, antes
 de que cualquier path operation la reciba.

Y también después de que se genere la response, antes de devolverla.

Por ejemplo, podrías añadir un custom header
 X-Process-Time que contenga el tiempo en segundos
 que tomó procesar la request y generar una response:
 # Example:
 import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
###
Aquí usamos time.perf_counter() en lugar de time.time()
 porque puede ser más preciso para estos casos de uso.
###
"""
# Orden de ejecucion de Multiples Middlewares
"""
Cuando añades múltiples middlewares usando ya
 sea el decorador @app.middleware() o el método
 app.add_middleware(), cada nuevo middleware envuelve
 la aplicación, formando un stack. El último middleware
 añadido es el más externo, y el primero es el más interno.

En el camino de la request, el middleware más externo se ejecuta primero.

En el camino de la response, se ejecuta al final
Por ejemplo:
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
Esto da como resultado el siguiente orden de ejecución:

Request: MiddlewareB → MiddlewareA → ruta

Response: ruta → MiddlewareA → MiddlewareB
* Este comportamiento de apilamiento asegura
   que los middlewares se ejecuten en un orden predecible y controlable.
"""
