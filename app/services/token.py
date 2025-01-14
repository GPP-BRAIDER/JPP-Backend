from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.token import TokenData

SECRET_KEY = "e1f880f051502d654fa005596d1ca4497f9fd1d4a91681de42230dd86522f3442161c023eaf7655266495c96ebb4a5c6543ea1a5523062af6559b7b4ac23e1a58114a1893cb799825e6d69a10f0fb1dd7a6e0bc38880688d397e284df58dbf2dfd43013847548abc4296553b536fbb1775b15bd918cd17af6c9653f168dc2f3f55fc13410c35bd93fdc07fcffa3e9ccce1690ea1ce2b88c1609b836e990099a3b51472935c17a14c974017b261cc1868c1f0c92ec9d518785de6d411d99a102d34573627b12c848d89a1be19389d96d1ccba5a270bc07abf3f419ce3db061be752cb0f005519f0023f4f318849cde7f2a05fa7a18bf7cdf7f58c2a9525c61427"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception