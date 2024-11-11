import pytest
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from documents import Employee
from bson import ObjectId
from unittest.mock import MagicMock
from services.v1.store_service import StoreService as StoreServiceV1
from exceptions import MissingDoc, UniqueKey, InvalidParam
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261


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
