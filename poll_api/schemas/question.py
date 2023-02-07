from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from poll_api.schemas.choice import Choice, ChoiceBase


class QuestionCreate(BaseModel):
    """Properties to receive via API on creation
    """
    text: str = Field(max_length=150)
    choices: List[ChoiceBase]


class QuestionUpdate(BaseModel):
    """Properties to receive via API on update
    """
    text: str = Field(max_length=150)


class Question(QuestionCreate):
    """Properties to return via API
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    choices: List[Choice]

    class Config:
        orm_mode = True
