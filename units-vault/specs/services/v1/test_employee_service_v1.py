import pytest
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from documents import Employee
from security import HashManager
from bson import ObjectId
from unittest.mock import MagicMock
from services.v1.store_service import StoreService as StoreServiceV1
from exceptions import MissingDoc, UniqueKey, InvalidParam
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261
import constants


class TestCreateV1:
    def test_should_create(self, mocker):
        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        service = EmployeeServiceV1()

        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(StoreServiceV1, 'get', return_value=magic_store)

        employee = service.create(creation_data)

        assert employee.id

    def test_should_create_with_password(self, mocker):
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

        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(StoreServiceV1, 'get', return_value=magic_store)

        mocker.patch.object(
            Employee,
            'save',
            return_value=True
        )

        mocker.patch.object(
            Employee,
            'validate',
            return_value=True
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__validate_unique_fields',
            return_value=True
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store_id',
            return_value=magic_store.id
        )

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

        mocker.patch.object(
            StoreServiceV1,
            'get',
            side_effect=MissingDoc('Store not found.')
        )

        with pytest.raises(MissingDoc) as error:
            service.create(creation_data)

        assert error.value.message == 'Store not found.'

    def test_should_fail_when_already_exist_by_document(self, mocker):
        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(
            StoreServiceV1,
            'get',
            return_value=magic_store
        )

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            return_value=MagicMock()
        )

        service = EmployeeServiceV1()

        with pytest.raises(UniqueKey) as error:
            service.create(creation_data)

        assert error.value.message == 'The document has already been taken.'

    def test_should_fail_when_already_exist_by_username(self, mocker):
        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "ADMIN"
        }

        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(
            StoreServiceV1,
            'get',
            return_value=magic_store
        )

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=MagicMock()
        )

        service = EmployeeServiceV1()

        with pytest.raises(UniqueKey) as error:
            service.create(creation_data)

        assert error.value.message == 'The username has already been taken.'

    def test_should_fail_when_invalid_role(self, mocker):
        creation_data = {
            "store_unit": 1,
            "name": "victor",
            "document": human_doc,
            "username": "victor-0x29a",
            "role": "INVALID"
        }

        service = EmployeeServiceV1()

        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(StoreServiceV1, 'get', return_value=magic_store)

        with pytest.raises(InvalidParam) as error:
            service.create(creation_data)

        expected_msg = 'The role is invalid, valid roles are: ADMIN, FINANCIAL, INVENTOR, OPERATOR'

        assert error.value.message == expected_msg


class TestDeleteV1:
    def test_should_delete(self, mocker):
        magic_employee = MagicMock()

        magic_employee.delete = MagicMock()

        mocker.patch.object(EmployeeServiceV1, 'get_by_document', return_value=magic_employee)

        mocker.patch.object(EmployeeServiceV1, 'delete')

        EmployeeServiceV1.delete('123456')

        assert True

    def test_should_fail_when_employee_not_found(self, mocker):
        magic_employee = MagicMock()

        magic_employee.first.return_value = None

        mocker.patch.object(
            Employee,
            'objects',
            return_value=magic_employee
        )

        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().delete('123456')

        assert error.value.message == 'Employee not found.'


class TestFillPasswordV1:
    def test_should_fill_password(self, mocker):
        magic_employee = MagicMock()

        magic_employee.password = None

        magic_employee.save.return_value = True

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            return_value=magic_employee
        )

        service = EmployeeServiceV1()

        password = 'password'

        hashed_password = service.fill_password('123456', password)

        assert hashed_password != password

    def test_should_fail_when_has_already_filled_password(self, mocker):
        magic_employee = MagicMock()

        magic_employee.password = 'password'

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            return_value=magic_employee
        )

        with pytest.raises(InvalidParam) as error:
            EmployeeServiceV1().fill_password('123456', 'password')

        assert error.value.message == 'Failed on process.'

    def test_should_fail_when_unexistent_employee(self, mocker):
        mocker.patch.object(
            Employee,
            'objects',
            side_effect=MissingDoc('Employee not found.')
        )

        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().fill_password('123456', 'password')

        assert error.value.message == 'Employee not found.'


class TestLoginV1:
    def test_should_generate_token(self, mocker):
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

        hash_manager = HashManager()

        magic_employee = MagicMock()

        magic_employee.document = human_doc

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        magic_employee.password = hash_manager.hash_passwd(login_data['password'])

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store',
            return_value=magic_store
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

        hash_manager = HashManager()

        magic_employee = MagicMock()

        magic_employee.document = human_doc

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        magic_employee.password = hash_manager.hash_passwd(login_data['password'])

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            return_value=magic_employee
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store',
            return_value=magic_store
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

        hash_manager = HashManager()

        magic_employee = MagicMock()

        magic_employee.document = human_doc

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        magic_employee.password = hash_manager.hash_passwd(login_data['password'])

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store',
            return_value=magic_store
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

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            side_effect=MissingDoc('Employee not found.')
        )

        with pytest.raises(MissingDoc) as error:
            EmployeeServiceV1().login(
                username=login_data['username'],
                password=login_data['password'],
                document=None
            )

        assert error.value.message == 'Employee not found.'

    def test_should_fail_when_unexist_store(self, mocker):
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

        hash_manager = HashManager()

        magic_employee = MagicMock()

        magic_employee.document = human_doc

        magic_employee.password = hash_manager.hash_passwd(login_data['password'])

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store',
            side_effect=MissingDoc('Store not found.')
        )

        service = EmployeeServiceV1()

        with pytest.raises(MissingDoc) as error:
            service.login(
                username=login_data['username'],
                password=login_data['password'],
                document=None
            )

        assert error.value.message == 'Store not found.'

    def test_should_login_when_havent_password(self, mocker):
        login_data = {
            'username': 'victor-0x29a'
        }

        jwt_secret = 'jwt_secret'

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            jwt_secret
        )

        magic_employee = MagicMock()

        magic_employee.document = human_doc

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        magic_employee.password = None

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            EmployeeServiceV1,
            '_EmployeeService__fetch_store',
            return_value=magic_store
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
