from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    tags: List[str] = []
    metadata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None

@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "id": id,
        "data": blog,
        "version": version
    }

@router.post("/new/{id}/comment/{comment_id}")
def create_comment(blog: BlogModel,
                   id: int,
                   comment_title: int = Query(None,
                                              title="Id of the comment",
                                              description="Description for comment title",
                                              alias="commentTitle"),
                   content: str = Body(Ellipsis,
                                       min_length=10,
                                       max_length=50,
                                       regex="^[a-z\s]*$"),
                   version: Optional[List[str]] = Query(["1.1", "1.2", "2.0"]),
                   comment_id: int = Path(None, gt=5, le=10)):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": version,
        "comment_id": comment_id
    }
