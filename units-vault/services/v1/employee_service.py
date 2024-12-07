from bson import ObjectId
from security import HashManager, SignatureManager
from documents import Employee, Store
from repositories import StoreRepository, EmployeeRepository
from exceptions import MissingDoc, InvalidParam
from constants import JWT_SECRET


class EmployeeService:
    def __init__(self):
        self.store_repository = StoreRepository(store_document=Store)
        self.repository = EmployeeRepository(employee_document=Employee)

    def create(self, data: dict) -> Employee:
        self.payload = data

        store_unit = self.payload.get('store_unit', None)

        if not isinstance(store_unit, int):
            raise MissingDoc('Store not found.')

        data['store_unit'] = self.__fetch_store_id()

        employee = self.repository.create(data=self.payload)

        return employee

    def delete(self, employee_document: str) -> None:
        employee = self.repository.get(filter={
            'document': employee_document
        })

        self.repository.delete(employee=employee)

    def fill_password(self, employee_document: str, password: str):
        employee = self.repository.get(filter={
            'document': employee_document
        })

        self.__check_can_fill_password(employee=employee)

        hash_manager = HashManager()

        hashed_password = hash_manager.hash_passwd(content=password)

        employee.password = hashed_password

        employee.save()

        return hashed_password

    def login(self, username: str, document: str, password: str):
        employee = None

        if username:
            employee = self.repository.get(filter={
                'username': username
            })
        if document and not employee:
            employee = self.repository.get(filter={
                'document': document
            })

        if not employee:
            raise MissingDoc('Employee document or username is required.')

        signature_manager = SignatureManager(secret=JWT_SECRET)

        if not employee.password:
            return signature_manager.sign(
                payload=self.__fetch_personal_info(employee),
                is_temporary=True
            )

        hash_manager = HashManager()

        is_valid_passwd_comparison = hash_manager.is_valid_hash_comparison(
            password,
            employee.password
        )

        if not is_valid_passwd_comparison:
            raise InvalidParam('Failed on process.')

        return signature_manager.sign(
            payload=self.__fetch_personal_info(employee)
        )

    def __check_can_fill_password(self, employee: Employee) -> None:
        has_password = employee.password is not None

        if has_password:
            raise InvalidParam('Failed on process.')

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
        store = self.store_repository.get(filter=filters)

        return store

    def __fetch_store_id(self) -> ObjectId:
        store_unit = self.payload.get('store_unit', None)
        store = self.__fetch_store({'unit': store_unit})

        return store.id
