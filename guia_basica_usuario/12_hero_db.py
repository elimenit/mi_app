from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

"""
table=True le dice a SQLModel que este es un modelo de tabla,
que debe representar una tabla en la base de datos SQL, no es solo 
un modelo de datos (como lo sería cualquier otra clase regular de Pydantic).

Field(primary_key=True) le dice a SQLModel que id es la clave primaria
 en la base de datos SQL (puedes aprender más sobre claves primarias de SQL
  en la documentación de SQLModel).

Nota: Usamos int | None para el campo de clave primaria para que en el código
 Python podamos crear un objeto sin un id (id=None), asumiendo que la base de
  datos lo generará al guardar. SQLModel entiende que la base de datos
   proporcionará el id y define la columna como un INTEGER no nulo
    en el esquema de la base de datos. Consulta la documentación de SQLModel
     sobre claves primarias para más detalles.

Field(index=True) le dice a SQLModel que debe crear un índice SQL para 
esta columna, lo que permitirá búsquedas más rápidas en la base de 
datos cuando se lean datos filtrados por esta columna.

SQLModel sabrá que algo declarado como str será una columna SQL
 de tipo TEXT (o VARCHAR, dependiendo de la base de datos).
"""
###
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
"""
Un engine de SQLModel (en el fondo, realmente es un engine
 de SQLAlchemy) es lo que mantiene las conexiones a la base de datos.
"""
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
###
"""
Usar check_same_thread=False permite a FastAPI usar la misma base de
 datos SQLite en diferentes hilos. 
Esto es necesario ya que una sola request podría usar más de 
un hilo (por ejemplo, en dependencias
"""

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

"""
añadimos una función que usa SQLModel.metadata.create_all(engine) 
para crear las tablas para todos los modelos de tabla.
"""

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

"""
Una Session es lo que almacena los objetos en memoria 
y lleva un seguimiento de cualquier cambio necesario en los 
datos, luego usa el engine para comunicarse con la base de datos.

Crearemos una dependencia de FastAPI con yield que 
proporcionará una nueva Session para cada request.
 Esto es lo que asegura que usemos una sola session por request. 

Luego creamos una dependencia Annotated SessionDep 
para simplificar el resto del código que usará esta dependencia.
"""
# <!-- Hasta aqui despues para el siguiente capitulo -->
# Crearemos las tablas de la base de datos cuando arranque la aplicación.
"""
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
# example: 
# <------->

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
    -----------
    Aquí usamos la dependencia SessionDep (una Session) 
    para añadir el nuevo Hero a la instance Session, 
    comiteamos los cambios a la base de datos,
     refrescamos los datos en el hero y luego lo devolvemos.
# <---------->
"""

# paginacion
"""
LEER UNA CANTIDAD DETERMINADA:
Podemos leer Heros de la base de datos usando un select().
 Podemos incluir un limit y offset para paginar los resultados.

@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

LEER X UNIDAD:

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
# ELIMINAR:

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
"""
# ENCAPSULAR EL HEROE DE LA DB DEl PUBLICo
"""
# Code above omitted 👆

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str
# OJO 
class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
"""

# Crear con HeroCreate y devolver un HeroPublic¶
"""
Ahora que tenemos múltiples modelos, podemos actualizar las 
partes de la aplicación que los usan.

Recibimos en la request un modelo de datos HeroCreate,
 y a partir de él, creamos un modelo de tabla Hero.

Este nuevo modelo de tabla Hero tendrá los campos enviados
 por el cliente, y también tendrá un id generado por la base de datos.

Luego devolvemos el mismo modelo de tabla Hero tal cual 
desde la función. Pero como declaramos el response_model con
 el modelo de datos HeroPublic, FastAPI usará HeroPublic
  para validar y serializar los datos
# EXAMPLE:

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

"""
# OJO
"""
Ahora usamos response_model=HeroPublic en lugar de la anotación de
 tipo de retorno -> HeroPublic porque el valor que estamos
  devolviendo en realidad no es un HeroPublic.

Si hubiéramos declarado -> HeroPublic, tu editor y linter
 se quejarían (con razón) de que estás devolviendo
  un Hero en lugar de un HeroPublic.

Al declararlo en response_model le estamos diciendo a FastAPI
 que haga lo suyo, sin interferir con las anotaciones
  de tipo y la ayuda de tu editor y otras herramientas
"""

"""
Leer Heroes con HeroPublic¶
Podemos hacer lo mismo que antes para leer Heros, nuevamente, usamos
 response_model=list[HeroPublic] para asegurar que los datos
 se validen y serialicen correctamente.
Example:

@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
"""
# Leer Un Hero con HeroPublic
"""
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
"""
# Actualizar un Hero con HeroUpdate
"""
Podemos actualizar un héroe. Para esto usamos 
una operación HTTP PATCH.
Y en el código, obtenemos un dict con todos los datos enviados
 por el cliente, solo los datos enviados por el cliente, 
 excluyendo cualquier valor que estaría allí solo por ser 
 valores por defecto. Para hacerlo usamos 
 exclude_unset=True. Este es el truco principal. 

Luego usamos hero_db.sqlmodel_update(hero_data) para
 actualizar el hero_db con los datos de hero_data.
 # Example:
# PUT ???
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db
"""
# Eliminar un Hero de Nuevo
"""
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
"""