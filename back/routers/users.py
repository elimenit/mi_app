from fastapi import APIRouter, Path, Query, Body
from database.dbase import Database
# Dependecias
from dependencies.dependencie import SessionDep
# Modelos Publicos
from schema.user import UpsertUser, UpdateUser, CreateUser 
# Base de Datos
database_instance = Database()

router = APIRouter(prefix="/users")
"""
GET y DELETE NOT BODY

"""
@router.get(path="/{id}", response_model=UpsertUser)
def get_user(id: int = Path()) -> UpsertUser:
    return database_instance.obtener_usuario(user_id=id)

@router.post(path="/", response_model=UpsertUser)
def create_user(new_user: CreateUser = Body()):
    print(new_user.model_dump())
    return database_instance.crear_usuario(new_user)
    