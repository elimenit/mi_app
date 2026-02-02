from fastapi import FastAPI
from routers.users import router_user

app = FastAPI(prefix="/api")

app.include_router(router_user)