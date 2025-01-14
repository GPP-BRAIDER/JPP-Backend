from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.init_db import init_db
from app.routers.authentication import registration, login
from app.routers import test

app = FastAPI()

# Initializing database.
init_db()


origins = [
    "*"
]

# Basic cors.
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "https://example.com"], 
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers.
app.include_router(registration.router)
app.include_router(login.router)
app.include_router(test.router)