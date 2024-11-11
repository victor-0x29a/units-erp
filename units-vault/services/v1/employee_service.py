from mongoengine.errors import ValidationError
from bson import ObjectId
from security import HashManager, SignatureManager
from documents import Employee, Store
from .store_service import StoreService
from exceptions import MissingDoc, UniqueKey, InvalidParam
from docs_constants import EMPLOYEE_ROLES
from constants import JWT_SECRET


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

        hash_manager = HashManager()

        hashed_password = hash_manager.hash_passwd(content=password)

        employee.password = hashed_password

        employee.save()

        return hashed_password

    def login(self, username: str, document: str, password: str):
        employee = None

        if username:
            employee = self.get_by_username(username=username)
        if document and not employee:
            employee = self.get_by_document(document=document)

        if not employee or not password:
            raise MissingDoc('Employee document or employee username, and password is required.')

        hash_manager = HashManager()

        is_valid_passwd_comparison = hash_manager.is_valid_hash_comparison(
            password,
            employee.password
        )

        if not is_valid_passwd_comparison:
            raise InvalidParam('Failed on process.')

        signature_manager = SignatureManager(secret=JWT_SECRET)

        return signature_manager.sign(
            payload=self.__fetch_personal_info(employee)
        )

    def __check_can_fill_password(self, employee: Employee) -> None:
        has_password = employee.password is not None

        if has_password:
            raise InvalidParam('Failed on process.')

    def __validate_creation_fields(self) -> None:
        has_password = self.payload.get('password', None)

        if has_password:
            self.__fill_password()

    def __fill_password(self):
        hash_manager = HashManager()

        self.payload['password'] = hash_manager.hash_passwd(
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

    def __fetch_personal_info(self, employee: Employee) -> dict:
        store_unit = self.__fetch_store(
            {'unit': employee.store_unit.unit}
        ).unit

        return {
            'employee_document': employee.document,
            'employee_role': employee.role,
            'store_unit': store_unit
        }

    def __fetch_store(self, filters: dict) -> Store:
        store = StoreService().get(filters)

        return store

    def __fetch_store_id(self) -> ObjectId:
        store_unit = self.payload.get('store_unit', None)
        store = self.__fetch_store({'unit': store_unit})

        return store.id
