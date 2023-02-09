from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from poll_api.api.deps import get_active_user, get_db
from poll_api.api.utils import get_or_404
from poll_api.crud.choice import choice_crud
from poll_api.crud.vote import vote_crud
from poll_api.models import User
from poll_api.schemas import vote

router = APIRouter()


@router.get(
    path='/',
    response_model=List[vote.Vote],
    dependencies=[Depends(get_active_user)]
)
def get_list(
    question_id: int,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100
) -> Any:
    """Returns vote list
    """
    return vote_crud.get_list(
        db=db,
        question_id=question_id,
        offset=offset,
        limit=limit
    )


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=vote.Vote
)
def create(
    vote_in: vote.VoteBase,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> Any:
    """Creates vote
    """
    choice = choice_crud.get(db=db, id=vote_in.choice_id)

    if not choice or (choice.question_id != vote_in.question_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect choice or question'
        )
    if vote_crud.get_by_params(
        db=db,
        question_id=vote_in.question_id,
        user_id=cur_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User vote already exists for the question'
        )
    return vote_crud.create(db=db, obj_in=vote_in, user_id=cur_user.id)


@router.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    cur_user: User = Depends(get_active_user)
) -> None:
    """Deletes vote
    """
    vote = get_or_404(crud=vote_crud, db=db, id=id)

    if vote.user_id == cur_user.id:
        return vote_crud.delete(db=db, db_obj=vote)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have enough privileges"
    )
