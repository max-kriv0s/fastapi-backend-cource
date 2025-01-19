from datetime import date

from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.router import router
from app.hotels.rooms.dao import RoomsDAO


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRoomInfo]:
   return await RoomsDAO.find_all(hotel_id, date_from, date_to)
