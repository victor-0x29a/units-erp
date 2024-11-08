from mongoengine.errors import ValidationError
from bson import ObjectId
from documents import Employee
from .store_service import StoreService
from docs_constants import EMPLOYEE_ROLES
from exceptions import MissingDoc, UniqueKey, InvalidParam


class EmployeeService:
    def create(self, data: dict) -> Employee:
        data['store_unit'] = self.__fetch_store_id(data)

        self.__validate_unique_fields(data=data)

        employee = Employee(**data)

        try:
            employee.validate()
            employee.save()
        except ValidationError as error:
            if 'role' in error.errors.keys():
                valid_roles = ', '.join(list(EMPLOYEE_ROLES.values()))

                raise InvalidParam(f'The role is invalid, valid roles are: {valid_roles}')

            raise error

        return employee

    def __validate_unique_fields(self, data: dict) -> None:
        employee_by_document = self.get_by_document(
            document=data.get('document'),
            can_raises=False
        )

        if employee_by_document:
            raise UniqueKey('The document has already been taken.')

        employee_by_username = self.get_by_username(
            username=data.get('username'),
            can_raises=False
        )

        if employee_by_username:
            raise UniqueKey('The username has already been taken.')

    def __fetch_store_id(self, data: dict) -> ObjectId:
        store = StoreService().get({'unit': data.get('store_unit', None)})

        return store.id

    @staticmethod
    def delete(employee_document: str) -> None:
        employee = Employee.objects(document=employee_document)

        if not employee:
            raise MissingDoc('Employee not found.')

        employee.delete()

    def get_by_document(self, document: str, can_raises=True) -> Employee:
        employee = Employee.objects(document=document).first()

        if not employee and can_raises:
            raise MissingDoc('Employee not found.')

        return employee

    def get_by_username(self, username: str, can_raises=True) -> Employee:
        employee = Employee.objects(username=username).first()

        if not employee and can_raises:
            raise MissingDoc('Employee not found.')

        return employee
