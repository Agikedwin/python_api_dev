from datetime import datetime

from pydantic import  BaseModel, EmailStr, conint
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True,

class CreatePost(PostBase):
    #Inherites all the whole post-base
    pass
class UpdatePost(PostBase):
    title: str
    content: str
    published: bool = True,

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    # converts the sqlalchemy model to pandantic model (query to valid dict)
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    #Only returns the fields we need to return to the user
    #Also inherits other fields in PostBase
    created_at : datetime
    owner_id: int
    id: int
    owner: UserResponse

    #converts the sqlalchemy model to pandantic model (query to valid dict)
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)