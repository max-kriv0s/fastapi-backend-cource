from datetime import date

from sqlalchemy import select, and_, func, or_
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels
    
    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
         select(Rooms.hotel_id, func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
       )

        get_hotels_with_rooms = (
         # Код ниже можно было бы расписать так:
         # select(
         #     Hotels
         #     booked_hotels.c.rooms_left,
         # )
         # Но используется конструкция Hotels.__table__.columns. Почему? Таким образом алхимия отдает
         # все столбцы по одному, как отдельный атрибут. Если передать всю модель Hotels и
         # один дополнительный столбец rooms_left, то будет проблематично для Pydantic распарсить
         # такую структуру данных. То есть проблема кроется именно в парсинге ответа алхимии 
         # Пайдентиком.
        select(
               Hotels.__table__.columns,
               booked_hotels.c.rooms_left,
        )
        .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
        .where(
              and_(
                  booked_hotels.c.rooms_left > 0,
                  Hotels.location.ilike(f"%{location}%"),
               )
        )
        )
        async with async_session_maker() as session:
         # logger.debug(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
            