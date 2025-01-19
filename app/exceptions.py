from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreasyExistsException(BookingException):
   status_code=status.HTTP_409_CONFLICT
   details='Пользователь уже существует'

class IncorrectEmailOrPasswordException(BookingException):
   status_code=status.HTTP_401_UNAUTHORIZED
   detail='Неверная почта или пароль'

class TokenExpiredException(BookingException):
   status_code=status.HTTP_401_UNAUTHORIZED
   detail='Токен истек'

class TokenAbsentException(BookingException):
   status_code=status.HTTP_401_UNAUTHORIZED
   detail='Токен отсутствует'

class IncorrectTokenFormatException(BookingException):
   status_code=status.HTTP_401_UNAUTHORIZED
   detail='Неверный формат токена'

class UserIsNotPresentException(BookingException):
   status_code=status.HTTP_401_UNAUTHORIZED
   detail='Неверный формат токена'
   
class RoomCannotBeBooked(BookingException):
   status_code=status.HTTP_409_CONFLICT
   detail='Не осталось свободных номеров'
   
class HotelNotFoundException(BookingException):
   status_code=status.HTTP_404_NOT_FOUND
   detail='Отель с таким id не найден'