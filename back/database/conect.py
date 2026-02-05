from sqlmodel import SQLModel, existscreate_engine, Session
from schema.user import User

NAME_FILE = "database.db"
PATH_SQLITE = f"sqlite:///{NAME_FILE}"
connect_args = {"check_same_thread": False}

engine = create_engine(PATH_SQLITE, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

