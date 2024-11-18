import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from security import HashManager
from services.v1.employee_service import EmployeeService as EmployeeServiceV1
from services.v1.store_service import StoreService as StoreServiceV1
from main import app
from ...fixture import mongo_connection # noqa: F401, E261
import constants
from exceptions import MissingDoc

client = TestClient(app)


class TestLoginEmployeeIntegrationV1():
    def test_should_login(self, mocker):
        login_data = {
            "username": "test",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        magic_employee = MagicMock()

        magic_employee.password = HashManager().hash_passwd(content='test')

        magic_employee.document = '000005'

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            StoreServiceV1,
            'get',
            return_value=magic_store
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)

    def test_should_login_by_document(self, mocker):
        login_data = {
            "document": "000005",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        magic_employee = MagicMock()

        magic_employee.password = HashManager().hash_passwd(content='test')

        magic_employee.document = '000005'

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            return_value=magic_employee
        )

        mocker.patch.object(
            StoreServiceV1,
            'get',
            return_value=magic_store
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)

    def test_should_fail_when_unexists_employeer(self, mocker):
        login_data = {
            "document": "000005",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_document',
            side_effect=MissingDoc('Employee not found.')
        )

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/employee/login", json=login_data)

        assert error.value.message == 'Employee not found.'

    def test_should_fail_when_unexists_store(self, mocker):
        login_data = {
            "username": "test",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        magic_employee = MagicMock()

        magic_employee.password = HashManager().hash_passwd(content='test')

        magic_employee.document = '000005'

        magic_employee.role = 'ADMIN'

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            StoreServiceV1,
            'get',
            side_effect=MissingDoc('Store not found.')
        )

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/employee/login", json=login_data)

        assert error.value.message == 'Store not found.'

    def test_should_login_without_password(self, mocker):
        login_data = {
            "username": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        magic_employee = MagicMock()

        magic_employee.password = None

        magic_employee.document = '000005'

        magic_employee.role = 'ADMIN'

        magic_store = MagicMock()

        magic_store.unit = 1

        mocker.patch.object(
            EmployeeServiceV1,
            'get_by_username',
            return_value=magic_employee
        )

        mocker.patch.object(
            StoreServiceV1,
            'get',
            return_value=magic_store
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)
