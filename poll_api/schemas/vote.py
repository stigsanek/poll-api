from datetime import datetime

from pydantic import BaseModel


class VoteBase(BaseModel):
    """Base shared properties
    """
    choice_id: int


class Vote(VoteBase):
    """Properties to return via API
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True
