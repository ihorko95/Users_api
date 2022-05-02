import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import Optional




class User(BaseModel):
    name: str = Field(..., example="Name", min_length=3)
    email: EmailStr = Field(..., example="email@gmail.com", )
    password: str = Field(..., example="password")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    register_date: Optional[str] = None


class UserPut(UserUpdate):
    id: Optional[str] = None

class UserList(UserUpdate):
    id: str

