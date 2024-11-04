from pydantic import BaseModel


class CreateStore(BaseModel):
    name: str
    unit: int
    latitude: float = 0
    longitude: float = 0
