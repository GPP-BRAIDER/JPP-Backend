from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.login import Login
from app.services.password.hash import verify_password
from app.services.token import create_access_token
import logging

def login_user(db: Session, user: Login):
    """
    Authenticate a user and generate an access token.

    This function takes in a database session and user login credentials, 
    verifies the user's identity, and generates a JWT access token if 
    authentication is successful.

    Args:
        db (Session): Database session object used to query the database.
        user (Login): User login data containing email and password.

    Raises:
        HTTPException: If the user credentials are invalid or if there is a 
                       server error during the login process.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    try:
        # Query the database for a user with the provided email
        login_user = db.query(User).filter(User.email == user.email).first()
        if not login_user:
            # Raise an HTTPException if the email is not found
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # Verify the provided password against the stored hashed password
        if not verify_password(user.password, login_user.password):
            # Raise an HTTPException if the password is incorrect
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # Create a JWT access token for the authenticated user
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Log any unexpected errors for debugging purposes
        logging.error(f"Error during login: {e}")
        # Raise an HTTPException for a server error
        raise HTTPException(status_code=500, detail="Internal server error")
