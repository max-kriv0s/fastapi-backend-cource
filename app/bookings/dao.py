from datetime import date, timedelta

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.orm import joinedload

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings
    
    @classmethod
    async def find_all_with_images(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    # __table__.columns нужен для отсутствия вложенности в ответе Алхимии
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')
            
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
            
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None


# Функция для решения практического задания по Celery beat
@classmethod
async def find_need_to_remind(cls, days: int):
    """Список броней и пользователей, которым необходимо
    направить напоминание за `days` дней"""
    async with async_session_maker_nullpool() as session:
        query = (
            select(Bookings)
            .options(joinedload(Bookings.user))
            # Фильтр ниже выдаст брони, до начала которых остается `days` дней
            # В нашем пет-проекте можно брать все брони, чтобы протестировать функционал
            .filter(date.today() == Bookings.date_from - timedelta(days=days))
        )
        result = await session.execute(query)
        return result.mappings().all()