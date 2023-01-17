from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash

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
    return db.query(DbUser).all()


def get_one_user(id: int, db: Session):
    return db.query(DbUser).filter(DbUser.id == id).first()
