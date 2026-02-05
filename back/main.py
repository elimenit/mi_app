from fastapi import FastAPI
# Rutas o Endpoints de nuestro servidor
from routers import users
from database.conect import create_db_and_tables

app = FastAPI()
create_db_and_tables()
# Rutas
app.include_router(users.router)

@app.get(path="/main", status_code=200)
def main():
    return {"Hola:": "FastApi"}