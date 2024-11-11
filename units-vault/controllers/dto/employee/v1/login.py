from pydantic import BaseModel


class Login(BaseModel):
    username: str = None
    document: str = None
    password: str
