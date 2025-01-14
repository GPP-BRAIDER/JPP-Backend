from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.login import Login
from app.services.password.hash import verify_password
from app.services.token import create_access_token
import logging

def login_user(db: Session, user: Login):
    try:
        login_user = db.query(User).filter(User.email == user.email).first()
        if not login_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        if not verify_password(user.password, login_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")