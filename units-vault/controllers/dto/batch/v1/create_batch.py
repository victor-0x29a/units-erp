from pydantic import BaseModel


class CreateBatch(BaseModel):
    cnpj: str
    ref: str
    expiry_date: str
