from typing import Optional

from sqlalchemy.orm import Session

from poll_api.crud.base import CRUDBase
from poll_api.models.user import User
from poll_api.schemas.user import UserCreate, UserUpdate
from poll_api.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD for User
    """

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Create user

        Args:
            db (Session): Database session
            obj_in (UserCreate): UserCreate instance

        Returns:
            User: User instance
        """
        data = obj_in.dict()
        hashed_password = get_password_hash(data['password'])
        del data['password']

        data.update({'hashed_password': hashed_password})
        return super().create(db=db, obj_in=data)

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user

        Args:
            db (Session): Database session
            db_obj (User): User instance
            obj_in (UserUpdate): UserUpdate instance

        Returns:
            User: User instance
        """
        data = obj_in.dict(exclude_unset=True)

        if data.get('password'):
            hashed_password = get_password_hash(data['password'])
            del data['password']
            data.update({'hashed_password': hashed_password})

        return super().update(db=db, db_obj=db_obj, obj_in=data)

    def authenticate(
        self,
        db: Session,
        username: str,
        password: str
    ) -> Optional[User]:
        """Auth user

        Args:
            db (Session): Database session
            username (str): Username
            password (str): Password

        Returns:
            Optional[User]: User instance
        """
        user = db.query(self.model).filter(
            self.model.username == username
        ).first()

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


crud = CRUDUser(User)
