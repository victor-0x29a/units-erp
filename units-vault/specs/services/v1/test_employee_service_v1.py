import pytest
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from documents import Employee, Store
from repositories import StoreRepository, EmployeeRepository
from exceptions import MissingDoc, UniqueKey, InvalidParam
from ...__mocks__.constants import human_doc, human_doc_2
from ...fixture import mongo_connection # noqa: F401, E261
import constants


class TestCreateV1:
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        service = EmployeeServiceV1()

        employee = service.create(creation_data)

        assert employee.id

    def test_should_create_with_password(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        password = 'strongpassword'

        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN",
            "password": password
        }

        service = EmployeeServiceV1()

        employee = service.create(creation_data)

        assert employee.name == creation_data['name']
        assert employee.document == creation_data['document']
        assert employee.role == creation_data['role']
        assert employee.username == creation_data['username']

        assert employee.password
        assert employee.password != password

    def test_should_fail_when_havent_store_unit(self, mocker):
        creation_data = {
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        service = EmployeeServiceV1()

        with pytest.raises(MissingDoc) as error:
            service.create(creation_data)

        assert error.value.message == 'Store not found.'

    def test_should_fail_when_already_exist_by_document(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        service = EmployeeServiceV1()

        service.create(creation_data)

        creation_data['username'] = 'victor-0x29b'

        with pytest.raises(UniqueKey) as error:
            service.create(creation_data)

        assert error.value.message == 'The document has already been taken.'

    def test_should_fail_when_already_exist_by_username(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        service = EmployeeServiceV1()

        service.create(creation_data)

        creation_data['document'] = human_doc_2

        with pytest.raises(UniqueKey) as error:
            service.create(creation_data)

        assert error.value.message == 'The username has already been taken.'

    def test_should_fail_when_invalid_role(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "INVALID"
        }

        service = EmployeeServiceV1()

        with pytest.raises(InvalidParam) as error:
            service.create(creation_data)

        expected_msg = 'The role is invalid, valid roles are: ADMIN, FINANCIAL, INVENTOR, OPERATOR'

        assert error.value.message == expected_msg


class TestDeleteV1:
    def test_should_delete(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        employee_creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        employee_repository.create(data=employee_creation_data)

        EmployeeServiceV1().delete(employee_document=human_doc)

    def test_should_fail_when_employee_not_found(self, mocker):
        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().delete(human_doc)

        assert error.value.message == 'Employee not found.'


class TestFillPasswordV1:
    def test_should_fill_password(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        employee_creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        employee_repository.create(data=employee_creation_data)

        service = EmployeeServiceV1()

        password = 'password'

        hashed_password = service.fill_password(human_doc, password)

        assert hashed_password != password

    def test_should_fail_when_has_already_filled_password(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Foo store"
        })

        employee_creation_data = {
            "store_unit": store.pk,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN",
            "password": 'password'
        }

        employee_repository.create(data=employee_creation_data)

        with pytest.raises(InvalidParam) as error:
            EmployeeServiceV1().fill_password(human_doc, 'password')

        assert error.value.message == 'Failed on process.'

    def test_should_fail_when_unexistent_employee(self, mocker):
        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().fill_password(human_doc, 'password')

        assert error.value.message == 'Employee not found.'


class TestLoginV1:
    def test_should_generate_token(self, mocker):
        employee_repository = EmployeeRepository(employee_document=Employee)
        store_repository = StoreRepository(store_document=Store)

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "victor-0x29a",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": 'password'
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            'username': 'victor-0x29a',
            'password': 'password'
        }

        jwt_secret = 'jwt_secret'

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            jwt_secret
        )

        service = EmployeeServiceV1()

        token = service.login(
            username=login_data['username'],
            password=login_data['password'],
            document=None
        )

        assert token
        assert isinstance(token, str)

    def test_should_generate_token_by_document(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "victor-0x29a",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": 'password'
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            'document': human_doc,
            'password': 'password'
        }

        jwt_secret = 'jwt_secret'

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            jwt_secret
        )

        service = EmployeeServiceV1()

        token = service.login(
            document=login_data['document'],
            password=login_data['password'],
            username=None
        )

        assert token
        assert isinstance(token, str)

    def test_should_not_fail_when_have_username_and_doc(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "victor-0x29a",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": 'password'
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            'username': 'victor-0x29a',
            'password': 'password',
            'document': human_doc
        }

        jwt_secret = 'jwt_secret'

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            jwt_secret
        )

        service = EmployeeServiceV1()

        token = service.login(
            username=login_data['username'],
            password=login_data['password'],
            document=login_data['document']
        )

        assert token
        assert isinstance(token, str)

    def test_should_fail_when_unexist_employee(self, mocker):
        login_data = {
            'username': 'victor-0x29a',
            'password': 'password'
        }

        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().login(
                username=login_data['username'],
                password=login_data['password'],
                document=None
            )

        assert error.value.message == 'Employee not found.'

    def test_should_login_when_havent_password(self, mocker):
        employee_repository = EmployeeRepository(employee_document=Employee)
        store_repository = StoreRepository(store_document=Store)

        store_creation_data = {
            "unit": 1,
            "name": "Foo store"
        }

        store = store_repository.create(data=store_creation_data)

        employee_creation_data = {
            "document": human_doc,
            "name": "Foo",
            "username": "victor-0x29a",
            "role": "ADMIN",
            "store_unit": store.pk
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            'username': 'victor-0x29a'
        }

        jwt_secret = 'jwt_secret'

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            jwt_secret
        )

        service = EmployeeServiceV1()

        token = service.login(
            username=login_data['username'],
            password=None,
            document=None
        )

        assert token
        assert isinstance(token, str)

    def test_should_fail_when_havent_username_and_document(self, mocker):
        service = EmployeeServiceV1()

        with pytest.raises(MissingDoc) as error:
            service.login(
                username=None,
                password=None,
                document=None
            )

        assert error.value.message == 'Employee document or username is required.'
