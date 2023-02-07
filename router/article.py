from fastapi import APIRouter, Depends
from schemas import ArticleBase, ArticleDisplay, ArticleUserDisplay
from sqlalchemy.orm.session import Session
from db import db_article
from db.database import get_db
from schemas import UserBase
from auth.outh2 import get_current_user
from typing import Dict, List

router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)

@router.get("/{id}", response_model=ArticleUserDisplay)
def get_article(id: int,
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }

@router.post("/", response_model=ArticleDisplay)
def create_article(request: ArticleBase,
                   db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)
