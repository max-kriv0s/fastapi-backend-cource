from datetime import date
from fastapi import APIRouter, Request
from pydantic import TypeAdapter

from app.cache.cache import redis_cache
from app.exceptions import HotelNotFoundException
from app.hotels.schemas import SHotel, SHotelInfo
from app.hotels.dao import HotelDAO
from app.logger import logger


router = APIRouter(
   prefix='/hotels',
   tags=['Отели']
)

@router.get('/{location}')
@redis_cache(expire=20)
async def get_hotel_by_location(
   location: str,
   date_from: date,
   date_to: date,
   request: Request
) -> list[SHotelInfo]:
   try:
     logger.info(f"Received request for hotels in {location} from {date_from} to {date_to}")
     return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)
   except Exception as e:
        logger.error(f"Error in get_hotels: {e}", exc_info=True)
        raise

@router.get("/id/{hotel_id}", include_in_schema=True)
# Этот эндпоинт используется для фронтенда, когда мы хотим отобразить все
# номера в отеле и информацию о самом отеле. Этот эндпоинт как раз отвечает за информацию
# об отеле.
# В нем нарушается правило именования эндпоинтов: конечно же, /id/ здесь избыточен.
# Тем не менее, он используется, так как эндпоинтом ранее мы уже задали получение
# отелей по их локации вместо id.
# Через include_in_schema можно регулировать отображение в swagger
async def get_hotel_by_id(
   hotel_id: int,
) -> SHotel:
   hotel =  await HotelDAO.find_one_or_none(id=hotel_id)
   if not hotel:
      raise HotelNotFoundException
   return hotel