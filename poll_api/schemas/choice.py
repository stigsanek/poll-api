from datetime import datetime

from pydantic import BaseModel, Field


class ChoiceBase(BaseModel):
    """Base shared properties
    """
    text: str = Field(max_length=150)


class Choice(ChoiceBase):
    """Properties to return via API
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    question_id: int

    class Config:
        orm_mode = True
