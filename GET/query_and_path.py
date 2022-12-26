from fastapi import FastAPI
from typing import Optional

app = FastAPI()

"""
combining query and path params:

endpoint:
http://127.0.0.1:8000/blog/101/comments/1?valid=true&username=ray.santiago
"""

@app.get("/blog/{id}/comments/{comment_id}")
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {"message": f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"}
