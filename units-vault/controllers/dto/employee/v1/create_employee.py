from pydantic import BaseModel
from typing import Literal
from docs_constants import EMPLOYEE_ROLES


roles_available = EMPLOYEE_ROLES.values()


class CreateEmployee(BaseModel):
    full_name: str
    document: str
    username: str
    role: Literal[*roles_available]
    store: int
