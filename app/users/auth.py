from jose import jwt
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from pydantic import EmailStr

from app.users.dao import UsersDAO
from app.config import settings


pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET, settings.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.hashed_password):
        return None
    
    return user
