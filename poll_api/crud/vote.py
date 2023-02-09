from typing import List, Optional

from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase
from poll_api.models import Vote
from poll_api.schemas.vote import VoteBase


class CRUDVote(CRUDBase[Vote, VoteBase, VoteBase]):
    """CRUD for Vote
    """

    def get_by_params(
        self,
        db: Session,
        question_id: int,
        user_id: int
    ) -> Optional[Vote]:
        """Return vote by question id and user id

        Args:
            db (Session): Database session
            question_id (int): Question id
            user_id (int): User id

        Returns:
            Optional[Vote]: Vote instance
        """
        return db.query(self.model).filter(
            Vote.question_id == question_id,
            Vote.user_id == user_id
        ).first()

    def get_list(
        self,
        db: Session,
        question_id: int,
        offset: int = 0,
        limit: int = 100
    ) -> List[Vote]:
        """Return list vote

        Args:
            db (Session): Database session
            question_id (int): Question id
            offset (int, optional): Offset
            limit (int, optional): Limit

        Returns:
            List[Vote]: List Vote instance
        """
        return db.query(self.model).filter(
            Vote.question_id == question_id
        ).offset(offset).limit(limit).all()

    def create(
        self,
        db: Session,
        obj_in: VoteBase,
        user_id: int
    ) -> None:
        """Create vote

        Args:
            db (Session): Database session
            obj_in (VoteBase): VoteBase instance
            user_id (int): User id

        Returns:
            Question: Vote instance
        """
        data = obj_in.dict()
        data['user_id'] = user_id
        return super().create(db=db, obj_in=data)


vote_crud = CRUDVote(Vote)
