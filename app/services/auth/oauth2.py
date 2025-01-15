from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.token import verify_token


# OAuth2PasswordBearer defines the OAuth2 authentication scheme.
# The "tokenUrl" is set to "login", which means that the user will send their login credentials 
# to this URL to get the access token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    """
    Dependency function to retrieve the current user based on the provided access token.
    
    Arguments:
        data (str): The access token extracted from the request's Authorization header.

    Returns:
        The result of the `verify_token` function, which should verify the token's validity and
        return the current user data if valid.

    Raises:
        HTTPException: If the token is invalid, it raises an HTTP 401 Unauthorized error.
    """
    
    # Define an exception to be raised if credentials (token) cannot be validated.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # HTTP status 401: Unauthorized
        detail="Could not validate credentials",    # The error message for the client
        headers={"WWW-Authenticate": "Bearer"},     # Authentication scheme (Bearer token) specified in headers
    )

    # Verify the token's validity using the 'verify_token' function. If the token is invalid, it will raise 'credentials_exception'.
    return verify_token(data, credentials_exception)