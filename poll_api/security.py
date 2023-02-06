from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from poll_api.config import settings

ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """Return access token

    Args:
        subject (Union[str, Any]): Token subject
        expires_delta (timedelta, optional): Token expiration time

    Returns:
        str: Token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {'exp': expire, 'sub': str(subject)}
    return jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_password_hash(password: str) -> str:
    """Return password hash

    Args:
        password (str): Password

    Returns:
        str: Password hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifiy password

    Args:
        plain_password (str): Plain password
        hashed_password (str): Password hash

    Returns:
        bool: _description_
    """
    return pwd_context.verify(plain_password, hashed_password)
