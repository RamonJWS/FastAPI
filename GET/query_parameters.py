from fastapi import FastAPI
from typing import Optional

app = FastAPI()

"""
Query parameters appear at the end of a endpoint path after the "?"
the parameters are separated by &.

e.g. http://127.0.0.1:8000/blog/all?page=1&page_size=10

default values can be applied in the function args.
in the path we dont have to include page
e.g. http://127.0.0.1:8000/blog/all?page_size=56

optional parameters are similar
"""

@app.get("/blog/all")
def get_blogs(page: int, page_size: int):
    return {"message": f"all {page_size} blogs on page {page}"}

# default values used
@app.get("/blog/all")
def get_blogs(page_size: int, page: int = 1):
    return {"message": f"all {page_size} blogs on page {page}"}

# optional parameters
@app.get("/blog/all")
def get_blogs(page_size: int, page: Optional[int] = 1):
    return {"message": f"all {page_size} blogs on page {page}"}
