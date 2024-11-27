import pytest
from main import app
from documents import Employee, Store
from repositories import StoreRepository, EmployeeRepository
from exceptions import MissingDoc
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261
from ...__mocks__.test_client import create_test_client

client = create_test_client(app)


class TestDeleteEmployeeIntegrationV1():
    def test_should_delete(self, mocker):
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
            "store_unit": store.pk
        })

        response = client.delete(f"/v1/employee/{human_doc}")

        assert response.status_code == 204

        employee = employee_repository.get(filter={'document': human_doc}, can_raises=False)

        assert not employee

    def test_should_fail_when_employee_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.delete(f"/v1/employee/{human_doc}")

        assert error.value.message == 'Employee not found.'
