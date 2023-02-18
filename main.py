"""
This is the main file where the app will be running
"""

import uvicorn

from fastapi import FastAPI
from router import blog_get, blog_posts, user, article, product, file
from auth import authentication
from db import models
from db.database import engine
from exceptions import EmailException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog_get.router)
app.include_router(blog_posts.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(file.router)


# this creates the db, only created when the db doesn't exist already.
models.Base.metadata.create_all(engine)

# handle custom exceptions in a more user friendly way:
@app.exception_handler(EmailException)
def email_exception_handler(request: Request, exc: EmailException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.message}
    )

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/files', StaticFiles(directory='files'), name='files')

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
