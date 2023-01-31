from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
SECRET_KEY = os.getenv("OAUTH_SECRET_KEY")
ALGORITHM = os.getenv("OAUTH_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire
