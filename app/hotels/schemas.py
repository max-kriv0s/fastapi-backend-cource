from datetime import date
from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class SHotelInfo(SHotel):
    rooms_left: int

    # orm_mode поменял название во 2 версии Pydantic
    model_config = ConfigDict(from_attributes=True)