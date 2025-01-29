from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Computed, Date, ForeignKey
from app.database import Base
from datetime import date

class Bookings(Base):
    __tablename__ = 'bookings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('date_to - date_from'))
    
    user: Mapped['Users'] = relationship( back_populates='bookings')
    room: Mapped['Rooms'] = relationship(back_populates='bookings')
    
    def __str__(self):
        return f'Bookings #{self.id}'