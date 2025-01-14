from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import env
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.services.password.hash import hash_password
import re

def register_user(db: Session, user: UserSchema):
    """
    Registers a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserSchema): User schema containing the user details.

    Raises:
        HTTPException: If any validation fails, such as duplicate email or phone number,
                       invalid age, invalid email format, invalid password format, or
                       missing required fields.

    Returns:
        User: The newly created User object.
        TODO: Return a jwt barear and login to user account.
    """

    # Check if email or phone number is already registered
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Email already registered"
                        )
    
    if db.query(User).filter(User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Phone number already registered"
                        )
    
    # Check if user is old enough
    if user.age < env.MINIMUM_AGE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User must be at least {env.MINIMUM_AGE} years old")
    
    # Check email and password by regex templates
    emailregex = r"/[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/igm"
    if re.match(emailregex, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Invalid email"
                        )
    
    passwordregex = r"/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{minlength,maxlength}$/"
    if re.match(passwordregex, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Invalid password"
                        )
    
    # Validate that all required fields are filled
    required_fields = [
        user.first_name,
        user.last_name,
        user.email,
        user.password, 
        user.age,
        user.country,
        user.city,
        user.address, 
        user.postal_code,
        user.phone_number
    ]
    
    if any(field is None or field == '' for field in required_fields):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="All fields must be filled"
                        )

    # Create new user record
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        age=user.age,
        country=user.country,
        city=user.city,
        address=user.address,
        postal_code=user.postal_code,
        phone_number=user.phone_number,
        #role=user.role,
        points=0
    )

    # Add and commit new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
