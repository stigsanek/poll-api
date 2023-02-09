from typing import List, Tuple

from sqlalchemy import func, insert, text
from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase
from poll_api.models import Choice, Vote
from poll_api.schemas.choice import ChoiceBase


class CRUDChoice(CRUDBase[Choice, ChoiceBase, ChoiceBase]):
    """CRUD for Choice
    """

    def create(
        self,
        db: Session,
        obj_list: List[ChoiceBase],
        question_id: int,
        user_id: int
    ) -> None:
        """Create choices bulk

        Args:
            db (Session): Database session
            obj_list (List[ChoiceBase]): ChoiceBase instance list
            question_id (int): Question id
            user_id (int): User id
        """
        data = []
        for obj in obj_list:
            obj_in = obj.dict()
            obj_in.update({'question_id': question_id, 'user_id': user_id})
            data.append(obj_in)

        db.execute(insert(self.model), data)
        db.commit()

    def get_result(
        self,
        db: Session,
        question_id: int
    ) -> List[Tuple[Choice, int]]:
        """Return count votes for choices

        Args:
            db (Session): Database session
            question_id (int): Question id

        Returns:
            List[Tuple[Choice, int]]: Data
        """
        return db.query(
            self.model,
            func.count(Vote.choice_id).label('votes')
        ).outerjoin(
            Vote,
            self.model.id == Vote.choice_id
        ).filter(
            self.model.question_id == question_id
        ).group_by(
            self.model.id
        ).order_by(
            text('votes DESC')
        ).all()


choice_crud = CRUDChoice(Choice)
