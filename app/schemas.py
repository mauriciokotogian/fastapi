from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

# pydantic checks the object has this values otherwise throws an error or use the default values
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    
  
class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

class PostResponse(PostBase):
    
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    #needed to support sqlalchemy object response be parsed by pydantic
    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    


    