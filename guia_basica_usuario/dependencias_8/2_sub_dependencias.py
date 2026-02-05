# Primera dependencia
"""
Podrías crear una primera dependencia ("dependable") así:
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}
###
Declara un parámetro de query opcional q como un str, y luego simplemente lo devuelve.

Esto es bastante simple (no muy útil), pero
 nos ayudará a centrarnos en cómo funcionan las sub-dependencias.
###
"""
# Segunda dependencia, "dependable" y "dependant"
"""
Luego puedes crear otra función de dependencia (un "dependable")
 que al mismo tiempo declare una dependencia 
 propia (por lo que también es un "dependant")

:
###
* Aunque esta función es una dependencia ("dependable")
   en sí misma, también declara otra dependencia (depende de algo más).
   Depende del query_extractor, y asigna el valor que devuelve al parámetro q.
* También declara una last_query cookie opcional, como un str.
   Si el usuario no proporcionó ningún query q, usamos 
   el último query utilizado, que guardamos previamente en una cookie.
###
"""
# Usando la Misma dependendcia multiples veces:
"""
Si una de tus dependencias se declara varias veces para
 la misma path operation, por ejemplo, múltiples dependencias
 tienen una sub-dependencia común, FastAPI sabrá llamar
 a esa sub-dependencia solo una vez por request.

Y guardará el valor devuelto en un "cache" y lo pasará a todos
 los "dependants" que lo necesiten en ese request específico,
  en lugar de llamar a la dependencia varias veces para el mismo request.

En un escenario avanzado donde sabes que necesitas que la
 dependencia se llame en cada paso (posiblemente varias veces)
 en el mismo request en lugar de usar el valor "cache", 
 puedes establecer el parámetro use_cache=False al usar Depends:
# Example:
async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
    return {"fresh_value": fresh_value}
"""
