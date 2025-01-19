from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Rooms(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]