import pytest
from unittest.mock import MagicMock
from mongoengine.errors import ValidationError
from bson import ObjectId
from ...__mocks__.test_client import create_test_client
from main import app
from documents import Employee, Store
from exceptions import MissingDoc
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261

client = create_test_client(app)


class TestCreateEmployeeIntegrationV1():
    def test_should_create(self, mocker):
        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_store
        )

        magic_employee = MagicMock()

        magic_employee.first.return_value = None

        mocker.patch.object(Employee, 'objects', return_value=magic_employee)

        mocker.patch.object(Employee, 'save', return_value=True)

        response = client.post("/v1/employee", json={
            "full_name": "Victor",
            "document": human_doc,
            "username": "victor w.",
            "role": "ADMIN",
            "store": 1
        })

        assert response.status_code == 204

    def test_should_fail_when_store_unexists(self, mocker):
        magic_store = MagicMock()

        magic_store.first.return_value = None

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_store
        )

        with pytest.raises(MissingDoc) as error:
            client.post("/v1/employee", json={
                "full_name": "Victor",
                "document": human_doc,
                "username": "victor w.",
                "role": "ADMIN",
                "store": 1
            })

        assert error

    def test_should_fail_when_is_an_invalid_role(self, mocker):
        response = client.post("/v1/employee", json={
            "full_name": "Victor",
            "document": human_doc,
            "username": "victor w.",
            "role": "ADMIN2",
            "store": 1
        })

        error = response.json()['errors'][0]

        assert response.status_code == 422
        assert error['field'] == "role"
        assert error['message'] == "Input should be 'ADMIN', 'FINANCIAL', 'INVENTOR' or 'OPERATOR'"

    def test_should_fail_when_document_is_invalid(self, mocker):
        magic_store = MagicMock()

        magic_store.id = ObjectId()

        mocker.patch.object(
            Store,
            'objects',
            return_value=magic_store
        )

        with pytest.raises(ValidationError) as error:
            client.post("/v1/employee", json={
                "full_name": "Victor",
                "document": '009',
                "username": "victor w.",
                "role": "ADMIN",
                "store": 1
            })

        assert "employee doc" in error.value.message
