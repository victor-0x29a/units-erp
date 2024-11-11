from pydantic import BaseModel


class FillPassword(BaseModel):
    password: str
