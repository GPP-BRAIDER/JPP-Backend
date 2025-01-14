from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user
from app.database.db import get_db
from app.repository.authentication import registration

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register", response_model=user.ShowUser)
def register(request: user.User, db: Session = Depends(get_db)):
    return registration.register_user(db, request)
