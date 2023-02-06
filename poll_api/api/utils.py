from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase, ModelType
from poll_api.models import User
from poll_api.schemas.user import UserCreate, UserUpdate


def get_or_404(crud: CRUDBase, db: Session, id: int) -> ModelType:
    """Helper for return item object from database by id

    Args:
        crud (CRUDBase): CRUDBase instance
        db (Session): Database session
        id (int): Item id

    Raises:
        HTTPException: If object not found

    Returns:
        ModelType: ModelType instance
    """
    obj = crud.get(db=db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
    return obj


def check_username(
    db: Session,
    user_in: Union[UserCreate, UserUpdate]
) -> None:
    """Check username exists

    Args:
        db (Session): Database session
        user_in (Union[UserCreate, UserUpdate]): Data

    Raises:
        HTTPException: If username exists
    """
    if hasattr(user_in, 'username'):
        if db.query(User).filter(User.username == user_in.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The user with this username already exists'
            )
