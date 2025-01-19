from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from datetime import datetime, UTC

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, UserIsNotPresentException

def get_token(req: Request) -> str:
   token = req.cookies.get('booking_access_token')
   if not token:
      raise TokenAbsentException
   return token

async def get_current_user(token: str = Depends(get_token)) -> Users:
   try:
      payload = jwt.decode(token, key=settings.ACCESS_TOKEN_SECRET, algorithms=settings.ACCESS_TOKEN_ALGORITHM)
   except JWTError:
      raise IncorrectTokenFormatException
   
   expire = payload.get('exp')
   if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
      raise TokenExpiredException
   
   user_id: str = payload.get('sub')
   if not user_id:
      raise UserIsNotPresentException
   
   user = await UsersDAO.find_by_id(int(user_id))
   if not user:
      raise UserIsNotPresentException
   
   return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
   # if current_user.role != 'admin':
   #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
   return current_user