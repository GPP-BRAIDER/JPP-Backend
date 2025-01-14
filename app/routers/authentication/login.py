from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.database.db import get_db
from app.services.password.hash import verify_password
from app.services.token import create_access_token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint for user authentication.
    - Accepts OAuth2PasswordRequestForm which contains `username`(email) and `password`.
    - Returns an access token upon successful authentication.

    Args:
        request (OAuth2PasswordRequestForm): The login form data.
        db (Session): The database session dependency.

    Returns:
        dict: A JSON object containing the access token and token type.
    """

    # Query the database for a user with the provided email (username).
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    # Verify the provided password with the hashed password stored in the database.
    if not verify_password(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    # Create a JWT access token for the authenticated user.
    access_token = create_access_token(data={"sub": user.email})

    # Return the generated access token and its type (bearer).
    return {"access_token": access_token, "token_type": "bearer"}
