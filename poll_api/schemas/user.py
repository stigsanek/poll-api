from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base shared properties
    """
    username: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Properties to receive via API on creation
    """
    username: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    password: str = Field(min_length=12, max_length=50)


class UserUpdate(UserBase):
    """Properties to receive via API on update
    """
    password: Optional[str] = Field(default=None, min_length=12, max_length=50)


class User(UserBase):
    """Properties to return via API
    """
    class Config:
        orm_mode = True
