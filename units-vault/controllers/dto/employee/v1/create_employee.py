from pydantic import BaseModel
from typing import Literal
from docs_constants import EMPLOYEE_ROLES


class CreateEmployee(BaseModel):
    full_name: str
    document: str
    username: str
    role: Literal[
        EMPLOYEE_ROLES['admin'],
        EMPLOYEE_ROLES['financial'],
        EMPLOYEE_ROLES['inventor'],
        EMPLOYEE_ROLES['operator']
    ]
    store: int
    password: str = None
