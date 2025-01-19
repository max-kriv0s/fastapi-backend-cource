from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    # orm_mode поменял название во 2 версии Pydantic
    model_config = ConfigDict(from_attributes=True)