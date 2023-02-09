from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, conlist

from poll_api.schemas.choice import Choice, ChoiceBase


class QuestionBase(BaseModel):
    """Base shared properties
    """
    text: str = Field(max_length=150)


class QuestionCreate(QuestionBase):
    """Properties to receive via API on creation
    """
    choices: conlist(ChoiceBase, min_items=2, max_items=10)


class Question(QuestionBase):
    """Properties to return via API for question list
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class QuestionItem(Question):
    """Properties to return via API for one question
    """
    choices: List[Choice]
