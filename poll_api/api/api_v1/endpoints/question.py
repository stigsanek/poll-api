from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from poll_api.api.deps import get_active_user, get_db
from poll_api.api.utils import get_or_404
from poll_api.crud.choice import choice_crud
from poll_api.crud.question import question_crud
from poll_api.models import User
from poll_api.schemas import question

router = APIRouter()


@router.get(
    path='/',
    response_model=List[question.Question],
    dependencies=[Depends(get_active_user)]
)
def get_list(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100
) -> Any:
    """Returns question list
    """
    return question_crud.get_list(db=db, offset=offset, limit=limit)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=question.QuestionItem
)
def create(
    question_in: question.QuestionCreate,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Creates question
    """
    question = question_crud.create(
        db=db,
        obj_in=question_in,
        user_id=cur_user.id
    )
    choice_crud.create(
        db=db,
        obj_list=question_in.choices,
        question_id=question.id
    )
    return question_crud.get(db=db, id=question.id)


@router.get(
    path='/{id}',
    response_model=question.QuestionItem,
    dependencies=[Depends(get_active_user)]
)
def get(
    id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Returns question by id
    """
    return get_or_404(crud=question_crud, db=db, id=id)


@router.patch(path='/{id}', response_model=question.Question)
def update(
    id: int,
    question_in: question.QuestionBase,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Updates question
    """
    question = get_or_404(crud=question_crud, db=db, id=id)

    if question.user_id == cur_user.id:
        return question_crud.update(db=db, db_obj=question, obj_in=question_in)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )


@router.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user),
) -> None:
    """Deletes question
    """
    question = get_or_404(crud=question_crud, db=db, id=id)

    if question.user_id == cur_user.id:
        question_crud.delete(db=db, db_obj=question)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
