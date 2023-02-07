from typing import List

from sqlalchemy import insert
from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase
from poll_api.models import Choice
from poll_api.schemas.choice import ChoiceBase


class CRUDChoice(CRUDBase[Choice, ChoiceBase, ChoiceBase]):
    """CRUD for Choice
    """

    def create(
        self,
        db: Session,
        obj_list: List[ChoiceBase],
        question_id: int
    ) -> None:
        """Create choices bulk

        Args:
            db (Session): Database session
            obj_list (List[ChoiceBase]): ChoiceBase instance list
            question_id (int): Question id
        """
        data = []
        for obj in obj_list:
            obj_in = obj.dict()
            obj_in.update({'question_id': question_id})
            data.append(obj_in)

        db.execute(insert(self.model), data)
        db.commit()


choice_crud = CRUDChoice(Choice)
