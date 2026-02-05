# FastApi
from fastapi import HTTPException

# Modelos Publicos
from schema.user import (
    UpsertUser, CreateUser, UpdateUser, DeleteUser,
    User
)
# Session para ejecutar querys a la base de datos

from dependencies.dependencie import SessionDep
class Database():
    def obtener_usuario(self, user_id: int, limit: int = 5, offset: int = 5) -> UpsertUser:
        """
        pre: 
            id: es un entero
        """
        user = self.get_session_dependecie.get(User, user_id)
        if user is None:
            raise HTTPException(detail="Usuario No Encontrado", status_code=404)  
        
        return UpsertUser(
            user_id = user.id,
            name = user.name,
            lastname = user.lastname,
            age = user.age
        )
    
    def get_session_dependecie(self) -> SessionDep:
        return SessionDep
    
    def crear_usuario(self, new_user: CreateUser) -> UpsertUser:
        session = self.get_session_dependecie()
        ## User 
        # user_create = User.model_validate(new_user)
        session.add(new_user)
        session.commit()
        session.refresh(user_create)
        return UpsertUser(
            user_id = user_create.id,
            name=user_create.name,
            lastname = user_create.lastname,
            age = user_create.age,
            email = user_create.email,
        )