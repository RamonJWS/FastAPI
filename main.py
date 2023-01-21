"""
This is the main file where the app will be running
"""

from fastapi import FastAPI
from router import blog_get, blog_posts, user, article
from db import models
from db.database import engine
from exceptions import EmailException
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_posts.router)
app.include_router(user.router)
app.include_router(article.router)

# this creates the db, only created when the db doesn't exist already.
models.Base.metadata.create_all(engine)

# handle custom exceptions in a more user friendly way:
@app.exception_handler(EmailException)
def email_exception_handler(request: Request, exc: EmailException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.message}
    )
