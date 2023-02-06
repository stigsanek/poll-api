from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base model
    """
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
