from fastapi import FastAPI
from app.database.init_db import init_db
from app.routers.authentication import registration, login
from app.routers import test

app = FastAPI()

init_db()

app.include_router(registration.router)
app.include_router(login.router)
app.include_router(test.router)