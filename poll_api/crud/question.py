from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase
from poll_api.models import Question
from poll_api.schemas.question import QuestionBase, QuestionCreate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionBase]):
    """CRUD for Question
    """

    def create(
        self,
        db: Session,
        obj_in: QuestionCreate,
        user_id: int
    ) -> Question:
        """Create question

        Args:
            db (Session): Database session
            obj_in (QuestionCreate): QuestionCreate instance
            user_id (int): User id

        Returns:
            Question: Question instance
        """
        data = obj_in.dict().copy()
        del data['choices']
        data['user_id'] = user_id
        return super().create(db=db, obj_in=data)


question_crud = CRUDQuestion(Question)
