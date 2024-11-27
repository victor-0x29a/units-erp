import pytest
from mongoengine.errors import ValidationError
from ...__mocks__.test_client import create_test_client
from main import app
from documents import Store
from repositories import StoreRepository
from exceptions import MissingDoc
from ...__mocks__.constants import human_doc
from ...fixture import mongo_connection # noqa: F401, E261

client = create_test_client(app)


class TestCreateEmployeeIntegrationV1():
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        response = client.post("/v1/employee", json={
            "full_name": "Victor",
            "document": human_doc,
            "username": "victor w.",
            "role": "ADMIN",
            "store": 1
        })

        assert response.status_code == 204

    def test_should_fail_when_store_unexists(self, mocker):
        with pytest.raises(MissingDoc) as error:
            client.post("/v1/employee", json={
                "full_name": "Victor",
                "document": human_doc,
                "username": "victor w.",
                "role": "ADMIN",
                "store": 1
            })

        assert error
        assert error.value.message == "Store not found."

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
        store_repository = StoreRepository(store_document=Store)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        with pytest.raises(ValidationError) as error:
            client.post("/v1/employee", json={
                "full_name": "Victor",
                "document": '009',
                "username": "victor w.",
                "role": "ADMIN",
                "store": 1
            })

        assert "employee doc" in error.value.message
