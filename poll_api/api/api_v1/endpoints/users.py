from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from poll_api.api.deps import get_db
from poll_api.api.utils import get_or_404
from poll_api.crud.user import crud
from poll_api.models.user import User
from poll_api.schemas import user

router = APIRouter()


@router.get('/', response_model=List[user.User])
def get_list(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100
) -> Any:
    """Returns user list
    """
    return crud.get_list(db=db, offset=offset, limit=limit)


@router.post('/', response_model=user.User)
def create(user_in: user.UserCreate, db: Session = Depends(get_db)) -> Any:
    """Creates user
    """
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this username already exists'
        )
    return crud.create(db=db, obj_in=user_in)


@router.get('/{id}', response_model=user.User)
def get(id: int, db: Session = Depends(get_db)) -> Any:
    """Returns user by id
    """
    return get_or_404(crud=crud, db=db, id=id)


@router.patch('/{id}', response_model=user.User)
def update(
    id: int,
    user_in: user.UserUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """Updates user
    """
    user = get_or_404(crud=crud, db=db, id=id)
    return crud.update(db=db, db_obj=user, obj_in=user_in)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)) -> None:
    """Deletes user
    """
    user = get_or_404(crud=crud, db=db, id=id)
    crud.delete(db=db, db_obj=user)
