from mongoengine import Document, StringField, ReferenceField, ValidationError
from pycpfcnpj import cpfcnpj
from .store import Store
from docs_constants import EMPLOYEE_ROLES


roles_available = [role for role in EMPLOYEE_ROLES.values()]


def is_valid_cpf(value):
    is_valid_cnpj = cpfcnpj.validate(value)

    if value and not is_valid_cnpj:
        raise ValidationError('The employee doc should be valid.')


class Employee(Document):
    name = StringField(required=True, max_length=60)
    document = StringField(required=True, validation=is_valid_cpf, unique=True)
    store_unit = ReferenceField(Store, required=True)
    username = StringField(required=True, max_length=30, unique=True)
    password = StringField(max_length=72, default=None)
    role = StringField(required=True, choices=roles_available)
