from mongoengine.errors import ValidationError
from bson import ObjectId
from documents import Employee
from .store_service import StoreService
from use_cases import CreateHashV1
from docs_constants import EMPLOYEE_ROLES
from exceptions import MissingDoc, UniqueKey, InvalidParam


class EmployeeService:
    def create(self, data: dict) -> Employee:
        self.payload = data

        data['store_unit'] = self.__fetch_store_id()

        self.__validate_unique_fields()

        self.__validate_creation_fields()

        employee = Employee(**self.payload)

        try:
            employee.validate()
            employee.save()
        except ValidationError as error:
            if 'role' in error.errors.keys():
                valid_roles = ', '.join(list(EMPLOYEE_ROLES.values()))

                raise InvalidParam(f'The role is invalid, valid roles are: {valid_roles}')

            raise error

        return employee

    def delete(self, employee_document: str) -> None:
        employee = self.get_by_document(document=employee_document)

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

    def fill_password(self, employee_document: str, password: str):
        employee = self.get_by_document(document=employee_document)

        self.__check_can_fill_password(employee=employee)

        create_hash = CreateHashV1()

        employee.password = create_hash.hash_passwd(content=password)

        employee.save()

    def __check_can_fill_password(self, employee: Employee) -> None:
        has_password = employee.password is not None

        if has_password:
            raise InvalidParam('Failed on process.')

    def __validate_creation_fields(self) -> None:
        has_password = self.payload.get('password', None)

        if has_password:
            self.__fill_password()

    def __fill_password(self):
        create_hash = CreateHashV1()

        self.payload['password'] = create_hash.hash_passwd(
            content=self.payload['password']
        )

    def __validate_unique_fields(self) -> None:
        employee_by_document = self.get_by_document(
            document=self.payload.get('document'),
            can_raises=False
        )

        if employee_by_document:
            raise UniqueKey('The document has already been taken.')

        employee_by_username = self.get_by_username(
            username=self.payload.get('username'),
            can_raises=False
        )

        if employee_by_username:
            raise UniqueKey('The username has already been taken.')

    def __fetch_store_id(self) -> ObjectId:
        store_unit = self.payload.get('store_unit', None)
        store = StoreService().get({'unit': store_unit})

        return store.id
