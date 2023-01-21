"""
This is the main file where the app will be running
"""

from fastapi import FastAPI
from router import blog_get, blog_posts, user, article
from db import models
from db.database import engine

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_posts.router)
app.include_router(user.router)
app.include_router(article.router)

# this creates the db, only created when the db doesn't exist already.
models.Base.metadata.create_all(engine)
