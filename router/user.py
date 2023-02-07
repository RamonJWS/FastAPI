from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List
from auth.outh2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

# read all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)

# read one user
@router.get("/{id}", response_model=UserDisplay)
def get_one_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_one_user(id, db)

# update user
@router.put("/{id}/update", response_model=UserDisplay)
def update_username(request: UserBase, id: int,
                    db: Session = Depends(get_db),
                    current_user: UserBase = Depends(get_current_user)):
    return db_user.update_user(request, db, id)

# delete user
@router.delete("/{id}/delete")
def delete_user(id: int,
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, id)

