from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class StoryCreate(BaseModel):
    title: str
    content: str

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Story(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes_count: Optional[int] = 0
    comments: Optional[list["Comment"]] = []

    model_config = {"from_attributes": True}

class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    story_id: int
    author: User

    model_config = {"from_attributes": True}

class LikeResponse(BaseModel):
    id: int
    user_id: int
    story_id: int
    created_at: datetime

    model_config = {"from_attributes": True}