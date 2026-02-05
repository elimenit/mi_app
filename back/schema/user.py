from sqlmodel import SQLModel, Field

class BaseUser(SQLModel):
    name: str = Field(index=True)
    lastname: str = Field(index=True) # apellido
    age: int | None = Field(default=None, index=True) # edad 

class User(BaseUser, table=True):
    # cuando se cree va ha ser user_id
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    password: str = Field(index=True)
    cv: str = Field(index=True)

class UpsertUser(BaseUser):
    user_id: int = Field(default=None) 
    email: str = Field(default=None)

# POST 
class CreateUser(BaseUser):
    email: str = Field()
    password: str = Field()
    cv: str = Field()

# PUT -> PATCH
class UpdateUser(BaseUser): # Actualizar
    name: str = Field(default=None)
    age: int = Field(default=None)
    password: str = Field(default= None)
    cv: str = Field(default=None)

# DELETE
class DeleteUser(BaseUser):
    password: str = Field(max_length=20, min_length=1)
    