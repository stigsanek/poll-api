from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from poll_api.api.deps import get_active_superuser, get_active_user, get_db
from poll_api.api.utils import get_or_404
from poll_api.crud.user import user_crud
from poll_api.models import User
from poll_api.schemas import user

router = APIRouter()


@router.get(
    path='/',
    response_model=List[user.User],
    dependencies=[Depends(get_active_superuser)]
)
def get_list(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100
) -> Any:
    """Returns user list
    """
    return user_crud.get_list(db=db, offset=offset, limit=limit)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=user.User
)
def create(user_in: user.UserCreate, db: Session = Depends(get_db)) -> Any:
    """Creates user
    """
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this username already exists'
        )
    user_in.is_superuser = False
    return user_crud.create(db=db, obj_in=user_in)


@router.get(path='/{id}', response_model=user.User)
def get(
    id: int,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Returns user by id
    """
    user = get_or_404(crud=user_crud, db=db, id=id)

    if user_crud.is_superuser(cur_user):
        return user
    if user == cur_user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )


@router.patch(path='/{id}', response_model=user.User)
def update(
    id: int,
    user_in: user.UserUpdate,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Updates user
    """
    user = get_or_404(crud=user_crud, db=db, id=id)

    if user_crud.is_superuser(cur_user):
        return user_crud.update(db=db, db_obj=user, obj_in=user_in)
    if user == cur_user:
        user_in.is_superuser = False
        return user_crud.update(db=db, db_obj=user, obj_in=user_in)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_active_superuser)]
)
def delete(id: int, db: Session = Depends(get_db)) -> None:
    """Deletes user
    """
    user = get_or_404(crud=user_crud, db=db, id=id)
    user_crud.delete(db=db, db_obj=user)
    user_crud.delete(db=db, db_obj=user)
