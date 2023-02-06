from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Base shared properties
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Properties to receive via API
    """
    sub: Optional[str] = None
