from pydantic import BaseModel
from typing import List

# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True

# new user
class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
    class Config:
        orm_mode = True

# user inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    class Config:
        orm_mode = True


class ArticleUser(BaseModel):
    id: int
    published: bool
    content: str
    title: str
    user_id: int
    class Config:
        orm_mode = True


class ArticleUserDisplay(BaseModel):
    data: ArticleUser
    current_user: User


class ProductBase(BaseModel):
    title: str
    description: str
    price: float