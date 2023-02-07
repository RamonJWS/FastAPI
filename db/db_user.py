from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException, status

def create_user(db: Session, request: UserBase):
    # dont need id as this is auto generated as primary key in models.py
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    # need to refresh because of id being primary key which is auto created for us.
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    all_users = db.query(DbUser).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found!")
    return db.query(DbUser).all()


def get_one_user(id: int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user


def update_user(request: UserBase, db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return db.query(DbUser).filter(DbUser.id == id).first()


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    db.delete(user)
    db.commit()
    return f"User with id: {id} has been deleted!"


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username: {username} not found")
    return user
