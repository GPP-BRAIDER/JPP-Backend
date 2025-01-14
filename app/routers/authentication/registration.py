from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user
from app.database.db import get_db
from app.repository.authentication import registration

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
async def register(request: user.User, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Accepts user details in the request body.
    - Returns the registered user data, adhering to the specified response model.

    Args:
        request (user.User): The input user data for registration, matching the `User` schema.
        db (Session): A database session provided by FastAPI's dependency injection.

    Returns:
        user.ShowUser: The registered user's generated Json Web Token.
    """

    # Passes the database session and user data to the registration logic.
    # This delegates the actual registration to a separate repository function.
    return registration.register_user(db, request)
