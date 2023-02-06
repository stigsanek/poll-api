from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base model
    """
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


class User(Base):
    """User model
    """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    questions: Mapped[List['Question']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
    votes: Mapped[List['Vote']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )


class Question(Base):
    """Question model
    """
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='questions')
    choices: Mapped[List['Choice']] = relationship(
        back_populates='question',
        cascade='all, delete-orphan'
    )


class Choice(Base):
    """Choice model
    """
    __tablename__ = 'choice'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    question: Mapped['Question'] = relationship(back_populates='choices')
    votes: Mapped[List['Vote']] = relationship(
        back_populates='choice',
        cascade='all, delete-orphan'
    )


class Vote(Base):
    """Vote model
    """
    __tablename__ = 'vote'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    choice_id: Mapped[int] = mapped_column(ForeignKey('choice.id'))
    choice: Mapped['Choice'] = relationship(back_populates='votes')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='votes')
