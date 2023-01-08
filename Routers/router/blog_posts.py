from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

@router.post("/new")
def create_blog(blog: BlogModel):
    return {"data": blog}
