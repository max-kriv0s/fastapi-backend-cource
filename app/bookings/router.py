from fastapi import APIRouter, Depends, status
from datetime import date

from app.bookings.schemas import SBooking, SBookingInfo
from app.bookings.dao import BookingDAO
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.get('/{booking_id}')
async def get_booking_by_id(booking_id: int) -> SBooking:
    return await BookingDAO.find_by_id(booking_id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)