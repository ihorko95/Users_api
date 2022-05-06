import uuid, re
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

pattern = {
    'id': '^((uuid4-[a-z]{4}\d)|([^\W_]{8}(-[^\W_]{4}){3}-[^\W_]{12}))$',
}


class User(BaseModel):
    name: str = Field(..., example="Name", min_length=3)
    email: EmailStr = Field(..., example="email@gmail.com")
    password: str = Field(..., example="password")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    register_date: Optional[str] = None


class UserList(UserUpdate):
    id: str = Field(..., description='The value does not match the template',
                    regex=pattern['id'])


class UserPut(UserUpdate, User):
    pass
