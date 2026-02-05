# session para gestionar la base de datos
from database.conect import get_session
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

# Instancia de la base de datos 