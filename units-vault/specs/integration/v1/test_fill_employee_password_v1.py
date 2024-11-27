from main import app
import pytest
from documents import Employee, Store
from repositories import EmployeeRepository, StoreRepository
from exceptions import MissingDoc, InvalidParam
from ...__mocks__.test_client import create_test_client
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261

client = create_test_client(app)


class TestFillEmployeePasswdIntegrationV1():
    def test_should_fill(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        employee = employee_repository.create(data={
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk
        })

        assert not employee.password

        update_data = {
            "password": "strongpassword"
        }

        response = client.put(f'/v1/employee/{human_doc}/password', json=update_data)

        assert response.status_code == 204

        employee.reload()

        assert employee.password
        assert isinstance(employee.password, str)

    def test_should_fail_when_already_is_filled(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        employee_repository = EmployeeRepository(employee_document=Employee)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        employee_repository.create(data={
            "document": human_doc,
            "name": "Foo",
            "username": "foo",
            "role": "ADMIN",
            "store_unit": store.pk,
            "password": "strongpassword"
        })

        update_data = {
            "password": "strongpassword"
        }

        with pytest.raises(InvalidParam) as error:
            client.put(f'/v1/employee/{human_doc}/password', json=update_data)

        assert error.value.message == 'Failed on process.'

    def test_should_fail_when_unexistent_employee(self, mocker):
        update_data = {
            "password": "strongpassword"
        }

        with pytest.raises(MissingDoc) as error:
            client.put(f'/v1/employee/{human_doc}/password', json=update_data)

        assert error.value.message == 'Employee not found.'
