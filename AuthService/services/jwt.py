from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from settings import JWT_CONFIG
from exceptions import InvalidTokenException, InvalidCredentialsException

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_CONFIG["SECRET_KEY"], algorithm=JWT_CONFIG["ALGORITHM"])
    return encoded_jwt

def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_CONFIG["SECRET_KEY"], algorithms=[JWT_CONFIG["ALGORITHM"]])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException
        return user_id
    except JWTError:
        raise InvalidCredentialsException
