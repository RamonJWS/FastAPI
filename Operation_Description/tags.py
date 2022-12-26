from fastapi import FastAPI
from typing import Optional
from config import TAGS_METADATA

app = FastAPI(openapi_tags=TAGS_METADATA)

"""
tags can be used to group REST operations together, this can be seen on the docs endpoint
we can create custom messages by passing openapi_tags argument to the app instance.

in the docs now the get_all will only be seen in the "blog" section, but the get_comment
can be seen in both.
"""

@app.get("/blog/{id}/comments/{comment_id}", tags=["blog", "comment"], response_description="test get_comment")
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {"message": f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"}
"""
response_description can be used for documentation in FASTapi docs.
docstring can be used to detail arguments if needed.
"""
@app.get("blog/all", tags=["blog"], response_description="test get_all")
def get_all():
    """
    **args** - None
    """
    return {"message": "returned all blogs"}
