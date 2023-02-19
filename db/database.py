import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import PROJECT_DIR

SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-practice.db"
# needed for testing...
SQLALCHEMY_DATABASE_URL_REL = 'sqlite:///' + os.path.join(PROJECT_DIR, 'fastapi-practice.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL_REL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# used to create our models.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
