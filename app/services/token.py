from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.token import TokenData
from app.env import *

def create_access_token(data: dict):
    """
    Creates a JWT access token with an expiration time.

    Arguments:
        data (dict): The data (usually user information) to include in the token payload.

    Returns:
        str: The encoded JWT access token as a string.
    """
    # Make a copy of the input data to avoid modifying the original.
    to_encode = data.copy()

    # Set the expiration time for the token.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Update the data to include the expiration time.
    to_encode.update({"exp": expire})

    # Encode the data into a JWT token using the specified secret key and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return the encoded JWT token.
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """
    Verifies and decodes a JWT token.

    Arguments:
        token (str): The JWT token to be verified.
        credentials_exception (HTTPException): The exception to be raised if the token is invalid.

    Returns:
        TokenData: The decoded token data (usually the user email).
    
    Raises:
        credentials_exception: If the token is invalid or expired, raises an exception.
    """
    try:
        # Decode the token and validate it using the secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the email (subject) from the payload.
        email: str = payload.get("sub")

        # If no email is found in the token payload, raise the credentials exception.
        if email is None:
            raise credentials_exception

        # Create an instance of TokenData with the extracted email.
        token_data = TokenData(email=email)

        # Return the token data.
        return token_data
    except JWTError:
        # If decoding the token fails (e.g., expired, tampered), raise the credentials exception.
        raise credentials_exception