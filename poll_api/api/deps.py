from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from poll_api.config import settings
from poll_api.crud.user import user_crud
from poll_api.db import SessionLocal
from poll_api.models import User
from poll_api.schemas.token import TokenPayload
from poll_api.security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1}/login')


def get_db() -> Generator:
    """Return database session

    Yields:
        Generator: Database session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Check token and return user

    Args:
        db (Session, optional): Database session
        token (str, optional): Token

    Returns:
        User: User instance
    """
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )

    user = user_crud.get(db=db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


def get_active_user(user: User = Depends(get_user)) -> User:
    """Check active user

    Args:
        user (User, optional): User instance

    Returns:
        User: User instance
    """
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    return user


def get_active_superuser(user: User = Depends(get_active_user)) -> User:
    """Check active superuser

    Args:
        user (User, optional): User instance

    Returns:
        User: User instance
    """
    if not user_crud.is_superuser(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return user
