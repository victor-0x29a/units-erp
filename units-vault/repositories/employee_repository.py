from documents import Employee
from security import HashManager
from mongoengine.errors import ValidationError
from exceptions import MissingDoc, MissingParam, InvalidParam, UniqueKey
from docs_constants import EMPLOYEE_ROLES
from copy import deepcopy


class EmployeeRepository:
    def __init__(self, employee_document: Employee):
        self.Employee = employee_document

    def get(self, filter=None, can_raises=True, is_only_one=True) -> Employee | list[Employee]:
        if not filter:
            raise MissingParam("Filter is required.")

        if is_only_one:
            employee = self.Employee.objects(**filter).first()
        else:
            employee = self.Employee.objects(**filter)

        if not employee and can_raises and is_only_one:
            raise MissingDoc("Employee not found.")

        return employee if is_only_one else list(employee)

    def create(self, data: dict) -> Employee:
        creation_data = deepcopy(data)

        self.__validate_unique_fields(data=creation_data)

        if creation_data.get('password', None):
            creation_data['password'] = self.__hash_password(
                password=creation_data['password']
            )

        employee = self.Employee(**creation_data)

        try:
            employee.validate()
            employee.save()
        except ValidationError as error:
            if 'role' in error.errors.keys():
                valid_roles = ', '.join(list(EMPLOYEE_ROLES.values()))

                raise InvalidParam(f'The role is invalid, valid roles are: {valid_roles}')

            raise error

        return employee

    def fill_password(self, employee: Employee, password: str) -> Employee:
        if not employee:
            raise MissingParam('Employee is required.')

        if employee.password:
            raise InvalidParam('Failed on process.')

        employee.password = self.__hash_password(password=password)

        employee.save()

        return employee

    def delete(self, employee: Employee) -> None:
        if not employee:
            raise MissingParam('Employee is required.')

        employee.delete()

    def __validate_unique_fields(self, data: dict):
        employee_by_document = self.get(
            filter={'document': data.get('document')},
            can_raises=False
        )

        if employee_by_document:
            raise UniqueKey('The document has already been taken.')

        employee_by_username = self.get(
            filter={'username': data.get('username')},
            can_raises=False
        )

        if employee_by_username:
            raise UniqueKey('The username has already been taken.')

    def __hash_password(self, password: str) -> str:
        hash_manager = HashManager()

        pwd_hash = hash_manager.hash_passwd(
            content=password
        )

        return pwd_hash
