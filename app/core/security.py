from typing import Any

from passlib.context import CryptContext
from app.config import settings
import jwt

pwd_context = CryptContext(
    schemes=['bcrypt'],
    default='bcrypt',
    bcrypt__rounds=14
)

def hash_password(password : str)->str:
    return pwd_context.hash(password)

def verify_password(password : str, hashed_password : str)->bool:
    return pwd_context.verify(secret=password,hash=hashed_password)


def create_access_token(payload : dict[str, Any]):
    try:
        token = jwt.encode(
            payload=payload,
            key=settings.ACCESS_TOKEN_SECRET,
            algorithm="HS256"
        )
        return token
    except Exception as e:
        raise
def create_refresh_token(payload : dict[str,Any]):
    try:
        token = jwt.encode(
            payload=payload,
            key=settings.REFRESH_TOKEN_SECRET,
            algorithm='HS256'
        )
        return token
    except Exception as e:
        raise