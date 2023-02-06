from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from poll_api.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Basic class for CRUD (Create, Read, Update, Delete) operations
    """

    def __init__(self, model: Type[ModelType]) -> None:
        """Initialization

        Args:
            model (Type[ModelType]): A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Return item by id

        Args:
            db (Session): Database session
            id (Any): Item id

        Returns:
            Optional[ModelType]: ModelType instance
        """
        return db.get(self.model, id)

    def get_list(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Return list items

        Args:
            db (Session): Database session
            offset (int, optional): Offset
            limit (int, optional): Limit

        Returns:
            List[ModelType]: List ModelType instance
        """
        return db.query(self.model).offset(offset).limit(limit).all()

    def create(
        self,
        db: Session,
        obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Create item

        Args:
            db (Session): Database session
            obj_in (Union[CreateSchemaType, Dict[str, Any]]): Data

        Returns:
            ModelType: ModelType instance
        """
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict()

        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update item

        Args:
            db (Session): Database session
            db_obj (ModelType): ModelType instance
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): Data

        Returns:
            ModelType: ModelType instance
        """
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)

        for k, v in data.items():
            setattr(db_obj, k, v)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        """Delete item

        Args:
            db (Session): Database session
            db_obj (ModelType): ModelType instance
        """
        db.delete(db_obj)
        db.commit()
