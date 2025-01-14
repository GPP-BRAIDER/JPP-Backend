from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.database.db import get_db

router = APIRouter(
    prefix="/bloge",
    tags=['Blogs']
)


#@router.get('/')
#def all(db: Session = Depends(get_db),current_user: user.User = Depends(oauth2.get_current_user)):
#    users = db.query(user.User).all()
#    return users

@router.get('/')
def all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users