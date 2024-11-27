from main import app
from fastapi.testclient import TestClient
import pytest
from repositories import EmployeeRepository, StoreRepository
from documents import Employee, Store
from exceptions import MissingDoc
import constants
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261

client = TestClient(app)


class TestLoginEmployeeIntegrationV1():
    def test_should_login(self, mocker):
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
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": 'test'
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            "username": "foo",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)

    def test_should_login_by_document(self, mocker):
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
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": 'test'
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            "document": human_doc,
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)

    def test_should_fail_when_unexists_employee(self, mocker):
        login_data = {
            "document": "000005",
            "password": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/employee/login", json=login_data)

        assert error.value.message == 'Employee not found.'

    def test_should_login_without_password(self, mocker):
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
            "username": "test",
            "role": "ADMIN",
            "store_unit": store.pk
        }

        employee_repository.create(data=employee_creation_data)

        login_data = {
            "username": "test"
        }

        mocker.patch.object(
            constants,
            'JWT_SECRET',
            'secret'
        )

        response = client.post("/v1/employee/login", json=login_data)

        assert response.status_code == 204
        assert response.headers['authorization']
        assert isinstance(response.headers['authorization'], str)
