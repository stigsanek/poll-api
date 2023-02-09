from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from poll_api.api.deps import get_active_user, get_db
from poll_api.api.utils import get_or_404
from poll_api.crud.choice import choice_crud
from poll_api.models import User
from poll_api.schemas import choice

router = APIRouter()


@router.get(
    path='/{id}',
    response_model=choice.Choice,
    dependencies=[Depends(get_active_user)]
)
def get(id: int, db: Session = Depends(get_db)) -> Any:
    """Returns choice by id
    """
    return get_or_404(crud=choice_crud, db=db, id=id)


@router.patch(path='/{id}', response_model=choice.Choice)
def update(
    id: int,
    choice_in: choice.ChoiceBase,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Updates choice
    """
    choice = get_or_404(crud=choice_crud, db=db, id=id)

    if choice.user_id == cur_user.id:
        return choice_crud.update(db=db, db_obj=choice, obj_in=choice_in)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )


@router.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> None:
    """Deletes choice
    """
    choice = get_or_404(crud=choice_crud, db=db, id=id)

    if choice.user_id == cur_user.id:
        return choice_crud.delete(db=db, db_obj=choice)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )
