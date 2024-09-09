from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    bar_code: str | None = None
    price: float
    base_stock: int
    batch: str
    discount_value: float = 0
    type: str
    for_use: str
