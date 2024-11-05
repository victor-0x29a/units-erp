from pydantic import BaseModel


class CreateBatch(BaseModel):
    store_unit: int
    cnpj: str
    ref: str
    expiry_date: str
