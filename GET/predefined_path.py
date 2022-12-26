from fastapi import FastAPI
from enum import Enum

app = FastAPI()

"""
The class allows for only specific types to be passed to the method below.
This is a way of restricting only certain values to be passed.
In the blow case it only allows strings in the 3 formats below.

Enums:
These are generally used to store data in a more pythonic way where we have
only specific values we want to choose from. Another example would be a Color class
with type str for green, blue, red, etc.
"""
class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"

@app.get("/blog/type/{type}")
def blog_type(type: BlogType):
    return {"message": f"blog type: {type}"}
