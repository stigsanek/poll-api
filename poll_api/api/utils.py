from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase, ModelType


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
