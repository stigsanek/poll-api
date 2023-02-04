from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import mapped_column

from poll_api.models.base import Base


class User(Base):
    """User model
    """
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), nullable=False, unique=True)
    first_name = mapped_column(String(50), nullable=False)
    last_name = mapped_column(String(50), nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True)
    is_superuser = mapped_column(Boolean, default=False)
