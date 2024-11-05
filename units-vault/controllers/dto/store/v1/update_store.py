from pydantic import BaseModel


class UpdateStore(BaseModel):
    name: str = None
    unit: int = None
    latitude: float = None
    longitude: float = None
