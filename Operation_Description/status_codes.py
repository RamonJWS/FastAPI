from fastapi import FastAPI, status, Response

app = FastAPI()

# status_code argument not super useful as we'd have to remember all of them
# instead use status.foo
# the other issue is that no matter what happens inside the function we will get the
# specified status code. We only want 404 if id > 5.

@app.get("/blog/{id}", status_code=status.HTTP_404_NOT_FOUND)
def get_blog(id: int):
    if id > 5:
        return {"error": f"blog {id} not found"}
    else:
        return {"message": f"blog with {id} found"}

"""
A better approach is to have response as an argument and set the response
depending on the logic.
"""

@app.get("/blog/{id}", status_code=status.HTTP_404_NOT_FOUND)
def get_blog_correct(id: int, response: Response):
    if id > 5:
        # e.g. not found in db
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"blog {id} not found"}
    else:
        # found in db
        response.status_code = status.HTTP_200_OK
        return {"message": f"blog with {id} found"}

